import os
import base64
import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from fastapi.responses import JSONResponse

from src.data.database import get_db
from src.model.population import PopulationStation, Place
from src.schema.population.population_schema import AgeGroupPopulationResponse, GenderPopulationResponse, PopulationRequest, PopulationResponse

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage

# 환경 변수 설정
from dotenv import load_dotenv
from src.data.database import env_activate

if env_activate:
    # Local 환경 설정
    api_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.env'))
    load_dotenv(api_path)
    endpoint = os.getenv('vision_endpoint')
    key = os.getenv('vision_api_key')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')

else:
    # Azure 환경 설정
    endpoint = os.getenv("vision_endpoint")
    key = os.getenv("vision_api_key")
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')


# Azure Vision API 클라이언트 생성
client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# FastAPI 라우터 생성
router = APIRouter(prefix="/vision", tags=["Vision API"])

# 시각적 특징 설정
visual_features = [
    VisualFeatures.DENSE_CAPTIONS,
]

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Svelte에서 업로드된 이미지를 Azure Vision API로 분석하고 결과를 반환합니다.
    """
    try:
        # 파일 읽기 (바이트 데이터 그대로 사용)
        image_data = await file.read()

        # Azure Vision API 호출 (바이트 데이터를 직접 전달)
        result = client.analyze(
            image_data=image_data,
            visual_features=visual_features,
            gender_neutral_caption=True,  # Optional
            language="en"
        )

        # 분석 결과 처리
        captions = []
        if result.dense_captions is not None:
            for caption in result.dense_captions.list:
                # bounding_box 객체의 속성 확인
                bbox = caption.bounding_box
                # print(dir(bbox))  # 속성 확인용 로그 출력

                # 속성 이름에 따라 값 추출
                captions.append({
                    "text": caption.text,
                    "confidence": caption.confidence,
                    "bounding_box": {
                        "x": bbox.x,
                        "y": bbox.y,
                        "w": bbox.width,
                        "h": bbox.height
                    }
                })

        # 바이트 데이터를 OpenCV에서 처리 가능한 이미지로 디코딩
        image_np = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

        # 이미지에 경계 상자와 캡션 표시
        colors = [
            (255, 0, 0),     # 파란색
            (0, 255, 0),     # 초록색
            (0, 0, 255),     # 빨간색
            (255, 255, 0),   # 청록색
            (255, 0, 255),   # 보라색
            (0, 255, 255)    # 노란색
        ]

        for idx, caption in enumerate(captions):
            bbox = caption["bounding_box"]
            x, y, w, h = int(bbox["x"]), int(bbox["y"]), int(bbox["w"]), int(bbox["h"])
            color = colors[idx % len(colors)]
            cv2.rectangle(image_np, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image_np, f"{caption['text']} ({caption['confidence']:.2f})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # 이미지를 메모리에서 처리
        _, buffer = cv2.imencode('.jpg', image_np)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        # 결과 반환
        return JSONResponse(content={
            "message": "이미지 분석 완료",
            "captions": captions,
            "image": image_base64  # Base64로 인코딩된 이미지
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 분석 중 오류 발생: {str(e)}")
    





def get_place_by_poi(db: Session, poi: str):
    return db.query(Place).filter(Place.place_id == poi).first()

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", """당신은 컨텍스트 정보를 사용해 사용자 이미지와 유사한 관광지를 추천하는 도우미입니다. 다음 지침을 따르세요:
                    1. 주어진 컨텍스트(지역명, 혼잡도, 혼잡도 메세지, 유동인구 데이터)를 기반으로 답변
                    2. 추천 받는 사람이 납득이 갈 수 있는 추천 메세지로 생성
                    3. 한국어로 100자 이내로 답변

                    컨텍스트: {contetxt}""")
    ]
)

# AzureChatOpenAI 모델 초기화
model = AzureChatOpenAI(
    azure_deployment="dev-gpt-35-turbo",
    api_version="2023-06-01-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

@router.post("/gpt/{region_id}")
async def get_gpt_response(
    region_id: str,
    db: Session = Depends(get_db)
):
    """
    특정 region_id의 PopulationStation 및 Place 데이터를 DB에서 가져와,
    이를 기반으로 AzureChatOpenAI의 GPT 모델을 단 한 번 호출하고, 응답을 반환합니다.
    """
    try:
        # region_id 유효성 검사
        if not region_id:
            raise HTTPException(status_code=400, detail="region_id가 제공되지 않았습니다.")

        # 1. PopulationStation 데이터 가져오기 (가장 최근 1개 레코드)
        query = (
            select(PopulationStation)
            .where(PopulationStation.region_id == region_id)
            .order_by(PopulationStation.datetime.desc())
            .limit(1)
        )
        result = await db.execute(query)
        record = result.scalars().first()

        if not record:
            raise HTTPException(status_code=404, detail="해당 region_id의 PopulationStation 데이터를 찾을 수 없습니다.")

        # 2. Place 테이블에서 해당 region_id에 해당하는 지역명 조회
        place_query = select(Place.name).where(Place.place_id == region_id)
        place_result = await db.execute(place_query)
        place_name = place_result.scalar()

        if not place_name:
            raise HTTPException(status_code=404, detail="해당 region_id의 장소 이름을 찾을 수 없습니다.")

        # 3. 지역 정보 반환
        data_info  = {
            "record": {
                "datetime": record.datetime.isoformat() if record.datetime else None,
                "region_id": record.region_id,
                "male_rate": record.male_rate,
                "female_rate": record.female_rate,
                "area_congest": record.area_congest,
                "congestion_message": record.congestion_message,
                "min_population": record.min_population,
                "max_population": record.max_population,
            },
            "place_name": place_name
        }

        
        # 4. 사용자 메시지에 컨텍스트 문자열을 포함하여 프롬프트 체인 구성
        context_str = f"""
        추천 지역명: {data_info['place_name']}
        혼잡도: {data_info['record']['area_congest']}
        혼잡도 메시지: {data_info['record']['congestion_message']}
        유동인구 데이터:
        - 남성 비율: {data_info['record']['male_rate']}
        - 여성 비율: {data_info['record']['female_rate']}
        - 최소 유동인구: {data_info['record']['min_population']}
        - 최대 유동인구: {data_info['record']['max_population']}
        """

        # 5. 각 요청마다 새로운 프롬프트 템플릿 인스턴스를 생성하여 메시지 체인 구성
        # 이전 요청의 상태가 남아있지 않고, 항상 깨끗한 상태로 메시지 체인을 구성
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """당신은 주어진 정보를 사용해 사용자 이미지와 유사한 관광지를 추천하는 도우미입니다.
            다음 지침을 따르세요:
            1. 주어진 컨텍스트(추천 지역명, 혼잡도, 혼잡도 메시지, 유동인구 데이터)를 반드시 보여주면서 대답
            2. 추천 지역명을 받는 사람이 납득할 수 있는 추천 메시지로 생성
            3. 한국어로 100자 이내로 간결하게 답변"""),
            MessagesPlaceholder(variable_name="messages")
        ])

        # HumanMessage를 사용하여 메시지 생성(메시지 리스트 초기화)
        messages = [HumanMessage(content=context_str)]

        # 프롬프트 템플릿을 사용하여 메시지 구성
        prompt = prompt_template.invoke({"messages": messages})

        # 5. GPT 모델 호출
        response = model.invoke(prompt)
        gpt_response = response.content

        # 6. 결과 반환
        return {"gpt_response": gpt_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")