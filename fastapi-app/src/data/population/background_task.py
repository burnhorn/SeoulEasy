import asyncio
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select
import time
import os
import sys
import httpx

# sys.path에 프로젝트 루트를 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..'))
sys.path.append(project_root)
print(f"프로젝트 루트 경로: {project_root}")

from src.model.population import PopulationStation as Population
from src.data.database import env_activate, get_db
# from dotenv import load_dotenv


# AREA_NM 리스트
# AREA_NM_LIST = [
#     "강남 MICE 관광특구", "동대문 관광특구", "명동 관광특구", "이태원 관광특구",
#     "잠실 관광특구", "종로·청계 관광특구", "홍대 관광특구", "경복궁",
#     "광화문·덕수궁", "보신각", "서울 암사동 유적", "창덕궁·종묘",
#     "강서한강공원", "고척돔", "광나루한강공원", "광화문광장",
#     "국립중앙박물관·용산가족공원", "난지한강공원", "남산공원", "노들섬",
#     "뚝섬한강공원", "망원한강공원", "반포한강공원", "북서울꿈의숲",
#     "불광천", "서리풀공원·몽마르뜨공원", "서울광장", "서울대공원",
#     "서울숲공원", "아차산", "양화한강공원", "어린이대공원",
#     "여의도한강공원", "월드컵공원", "응봉산", "이촌한강공원",
#     "잠실종합운동장", "잠실한강공원", "잠원한강공원", "청계산",
#     "청와대"
# ]

AREA_NM_LIST = [
    "강남 MICE 관광특구",
    "동대문 관광특구",
    "명동 관광특구",
    "이태원 관광특구",
    "잠실 관광특구",
    "종로·청계 관광특구",
    "홍대 관광특구",
    "경복궁",
    "광화문·덕수궁",
    "보신각",
    "서울 암사동 유적",
    "창덕궁·종묘",
    "가산디지털단지역",
    "강남역",
    "건대입구역",
    "고덕역",
    "고속터미널역",
    "교대역",
    "구로디지털단지역",
    "구로역",
    "군자역",
    "남구로역",
    "대림역",
    "동대문역",
    "뚝섬역",
    "미아사거리역",
    "발산역",
    "북한산우이역",
    "사당역",
    "삼각지역",
    "서울대입구역",
    "서울식물원·마곡나루역",
    "서울역",
    "선릉역",
    "성신여대입구역",
    "수유역",
    "신논현역·논현역",
    "신도림역",
    "신림역",
    "신촌·이대역",
    "양재역",
    "역삼역",
    "연신내역",
    "오목교역·목동운동장",
    "왕십리역",
    "용산역",
    "이태원역",
    "장지역",
    "장한평역",
    "천호역",
    "총신대입구(이수)역",
    "충정로역",
    "합정역",
    "혜화역",
    "홍대입구역(2호선)",
    "회기역",
    "4·19 카페거리",
    "가락시장",
    "가로수길",
    "광장(전통)시장",
    "김포공항",
    "낙산공원·이화마을",
    "노량진",
    "덕수궁길·정동길",
    "방배역 먹자골목",
    "북촌한옥마을",
    "서촌",
    "성수카페거리",
    "수유리 먹자골목",
    "쌍문동 맛집거리",
    "압구정로데오거리",
    "여의도",
    "연남동",
    "영등포 타임스퀘어",
    "외대앞",
    "용리단길",
    "이태원 앤틱가구거리",
    "인사동",
    "창동 신경제 중심지",
    "청담동 명품거리",
    "청량리 제기동 일대 전통시장",
    "해방촌·경리단길",
    "DDP(동대문디자인플라자)",
    "DMC(디지털미디어시티)",
    "강서한강공원",
    "고척돔",
    "광나루한강공원",
    "광화문광장",
    "국립중앙박물관·용산가족공원",
    "난지한강공원",
    "남산공원",
    "노들섬",
    "뚝섬한강공원",
    "망원한강공원",
    "반포한강공원",
    "북서울꿈의숲",
    "불광천",
    "서리풀공원·몽마르뜨공원",
    "서울광장",
    "서울대공원",
    "서울숲공원",
    "아차산",
    "양화한강공원",
    "어린이대공원",
    "여의도한강공원",
    "월드컵공원",
    "응봉산",
    "이촌한강공원",
    "잠실종합운동장",
    "잠실한강공원",
    "잠원한강공원",
    "청계산",
    "청와대",
    "북창동 먹자골목",
    "남대문시장",
    "익선동"
]


# AREA_NM_LIST = [
#     "강남 MICE 관광특구"
# ]

# 환경 변수 설정 (database.py에서 환경 변수 설정했으므로 다시 환경변수 프로젝트 위치 로드할 필요 없음)
if env_activate:
    ## local 환경 설정
    # .env 파일의 절대 경로를 지정합니다.
    # api_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.env'))

    # # .env 파일을 로드합니다.
    # load_dotenv(api_path)
    # print(dotenv_path)
    # 환경 변수를 가져옵니다.
    API_KEY = os.getenv('API_KEY')

else:
    # Azure 환경 설정
    API_KEY = os.getenv("API_KEY")

# API 요청 함수
# 이 함수는 비동기 함수(async def)로 정의
# 즉, 호출 시 즉시 실행되지 않고, 비동기 작업 객체(coroutine)를 반환
async def fetch_population_data(area_name: str, db: AsyncSession):
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        print(f"[{area_name}] 데이터 수집 시작")
        
        BASE_URL = "http://openapi.seoul.go.kr:8088"
        SERVICE = "citydata"
        START_INDEX = 1
        END_INDEX = 5

        url = f"{BASE_URL}/{API_KEY}/xml/{SERVICE}/{START_INDEX}/{END_INDEX}/{area_name}"
        print(f"요청 URL: {url}")
        
        try:
            response = await client.get(url)
            print(f"응답 상태 코드: {response.status_code}")
        except Exception as e:
            print(f"API 요청 에러: {e}")
            return
        
        # 요청 간 지연 시간 추가 (예: 1초)
        await asyncio.sleep(1)
        
        if response.status_code == 200:
            xml_data = response.text
            # print(f"응답 데이터: {xml_data}")
            root = ET.fromstring(xml_data)

            for citydata in root.findall(".//CITYDATA"):
                area_code = citydata.find("AREA_CD").text
                congestion_level = citydata.find(".//LIVE_PPLTN_STTS/AREA_CONGEST_LVL").text
                congestion_message = citydata.find(".//LIVE_PPLTN_STTS/AREA_CONGEST_MSG").text
                male_rate = citydata.find(".//LIVE_PPLTN_STTS//MALE_PPLTN_RATE").text
                female_rate = citydata.find(".//LIVE_PPLTN_STTS//FEMALE_PPLTN_RATE").text
                gen_10 = citydata.find(".//LIVE_PPLTN_STTS//PPLTN_RATE_10").text
                gen_20 = citydata.find(".//LIVE_PPLTN_STTS//PPLTN_RATE_20").text
                gen_30 = citydata.find(".//LIVE_PPLTN_STTS//PPLTN_RATE_30").text
                gen_40 = citydata.find(".//LIVE_PPLTN_STTS//PPLTN_RATE_40").text
                gen_50 = citydata.find(".//LIVE_PPLTN_STTS//PPLTN_RATE_50").text
                gen_60 = citydata.find(".//LIVE_PPLTN_STTS//PPLTN_RATE_60").text
                gen_70 = citydata.find(".//LIVE_PPLTN_STTS//PPLTN_RATE_70").text
                min_population = citydata.find(".//LIVE_PPLTN_STTS/AREA_PPLTN_MIN").text
                max_population = citydata.find(".//LIVE_PPLTN_STTS/AREA_PPLTN_MAX").text
                update_time = citydata.find(".//LIVE_PPLTN_STTS//PPLTN_TIME").text

                population = Population(
                    datetime=datetime.strptime(update_time, "%Y-%m-%d %H:%M"),
                    region_id=area_code,
                    male_rate=float(male_rate),
                    female_rate=float(female_rate),
                    area_congest=congestion_level,
                    congestion_message=congestion_message,
                    gen_10=float(gen_10),
                    gen_20=float(gen_20),
                    gen_30=float(gen_30),
                    gen_40=float(gen_40),
                    gen_50=float(gen_50),
                    gen_60=float(gen_60),
                    gen_70=float(gen_70),
                    min_population=int(min_population),
                    max_population=int(max_population),
                )
                print(f"수집 데이터: {population}")
                print(f"DB 세션 상태: {db}")
                existing_data = await db.execute(
                    select(Population).where(
                        Population.datetime == population.datetime,
                        Population.region_id == population.region_id
                    )
                )
                result = existing_data.scalars().first()
                if not result:
                    db.add(population)  # commit하기 전에 db 세션에 새 데이터를 추가
                    print("새 데이터를 데이터베이스에 추가했습니다.")
                else:
                     print("데이터베이스에 데이터가 저장되지 않았습니다.")

            try:
                await db.commit()
                print("데이터베이스 커밋 성공")
            except Exception as e:
                print(f"데이터베이스 커밋 에러: {e}")

        end_time = time.time()
        print(f"[{area_name}] 데이터 수집 완료 (소요 시간: {end_time - start_time:.2f}초)")


# #백그라운드 작업 (순차처리)
# async def background_task():
#     async for db in get_db():  # get_db를 사용하여 세션 생성
#         while True:
#             start_time = time.time()
#             print("데이터베이스 세션 생성 성공")
#             for area_name in AREA_NM_LIST:
#                 await fetch_population_data(area_name, db)
#             end_time = time.time()
#             print(f"전체 데이터 수집 완료 (소요 시간: {end_time - start_time:.2f}초)")
#             await asyncio.sleep(310)  # 5분 대기


# 병렬 처리 시 배치 크기 설정
BATCH_SIZE = 20

async def background_task():
    while True:
        start_time = time.time()

        # AREA_NM_LIST를 BATCH_SIZE 크기로 나눔
        for i in range(0, len(AREA_NM_LIST), BATCH_SIZE):
            batch = AREA_NM_LIST[i:i + BATCH_SIZE]  # 20개씩 나눔
            batch_tasks = []
            for area_name in batch:
                async for db in get_db():
                    # 배치 크기만큼 작업을 추가
                    # fetch_population_data 함수는 비동기 함수(async def)이므로 바로 실행되지 않음
                    # 실행을 위해 asyncio.create_task()로 작업 객체를 생성
                    # 작업 객체는 실행 준비 상태로 batch_tasks 리스트에 추가
                    batch_tasks.append(fetch_population_data(area_name, db))
            # 현재 배치의 작업을 병렬로 실행(여러 비동기 작업을 병렬로 실행 후 완료되면 다음 코드 진행)
            # API 요청은 네트워크 I/O 작업이므로 병렬로 실행하면 효율적
            # 네트워크 요청은 응답을 기다리는 동안 CPU를 사용하지 않으므로, 다른 작업을 동시에 실행할 수 있음
            await asyncio.gather(*batch_tasks)

        end_time = time.time()
        print(f"전체 데이터 수집 완료 (소요 시간: {end_time - start_time:.2f}초)")
        await asyncio.sleep(150)  # 2분 30초 대기