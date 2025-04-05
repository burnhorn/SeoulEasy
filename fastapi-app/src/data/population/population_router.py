from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.population import PopulationStation
from src.data.database import get_db
from src.schema.population.population_schema import AgeGroupPopulationResponse, GenderPopulationResponse, PopulationRequest, PopulationResponse
from sqlalchemy import func
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime, timedelta


router = APIRouter(prefix = "/populations")

# 페이징 처리(최근 200분 동안의 5분 간격 데이터)
@router.get("/region/{region_id}", response_model=list[PopulationResponse])
async def get_population_by_region(
    region_id: str,
    limit: int = 40,  # 한 번에 가져올 데이터 수
    offset: int = 0,   # 시작 위치
    db: AsyncSession = Depends(get_db)
):
    """
    특정 region_id의 데이터를 페이징하여 반환
    """
    query = (
        select(PopulationStation)
        .where(PopulationStation.region_id == region_id)
        .order_by(PopulationStation.datetime.desc())  # 최신 데이터 우선 정렬
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(query)
    records = result.scalars().all()
    return records

# 성별 인구 데이터 조회
@router.get("/gender_population_data", response_model=List[GenderPopulationResponse])
async def get_gender_population_data(
    region_id: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    특정 region_id와 시간 범위의 성별 데이터를 반환합니다.
    만약 start_time과 end_time이 전달되지 않으면, 기본적으로 현재 시각 기준 60분 전부터 현재 시각까지의 데이터를 조회합니다.
    """
    try:
        # 현재 시각 계산
        now = datetime.now()
        if start_time is None:
            start_time = (now - timedelta(minutes=60)).strftime("%H:%M:%S")
        if end_time is None:
            end_time = now.strftime("%H:%M:%S")
        
        # 쿼리: 특정 region_id와 지정된 시간 범위 내의 데이터를 가져옴
        query = select(PopulationStation).filter(
            PopulationStation.region_id == region_id,
            func.time(PopulationStation.datetime).between(start_time, end_time)
        )
        result = await db.execute(query)
        records = result.scalars().all()

        # 응답 데이터 구성
        response_data = [
            {
                "datetime": rec.datetime.isoformat() if rec.datetime else None,
                "region_id": rec.region_id,
                "male_min_population": rec.male_rate * rec.min_population / 100 if rec.min_population and rec.male_rate is not None else None,
                "male_max_population": rec.male_rate * rec.max_population / 100 if rec.max_population and rec.male_rate is not None else None,
                "female_min_population": rec.female_rate * rec.min_population / 100 if rec.min_population and rec.female_rate is not None else None,
                "female_max_population": rec.female_rate * rec.max_population / 100 if rec.max_population and rec.female_rate is not None else None,
            }
            for rec in records
        ]
        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")

# 성별 인구 데이터 조회 (최소 인구 수)
@router.get("/age_min_population_data", response_model=List[AgeGroupPopulationResponse])
async def get_age_group_min_population_data(
    region_id: str,
    limit: int = 40,  # 한 번에 가져올 데이터 수
    offset: int = 0,   # 시작 위치
    db: AsyncSession = Depends(get_db)
):
    """
    특정 region_id의 연령대별 최대 인구 데이터를 반환
    """
    query = (
        select(PopulationStation)
        .where(PopulationStation.region_id == region_id)
        .order_by(PopulationStation.datetime.desc())  # 최신 데이터 우선 정렬
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(query)
    records = result.scalars().all()
    # 응답 데이터 구성
    response_data = [
        {
            "datetime": rec.datetime.isoformat() if rec.datetime else None,
            "region_id": rec.region_id,
            "gen_10": rec.gen_10 * rec.min_population / 100 if rec.min_population and rec.gen_10 is not None else None,
            "gen_20": rec.gen_20 * rec.min_population / 100 if rec.min_population and rec.gen_20 is not None else None,
            "gen_30": rec.gen_30 * rec.min_population / 100 if rec.min_population and rec.gen_30 is not None else None,
            "gen_40": rec.gen_40 * rec.min_population / 100 if rec.min_population and rec.gen_40 is not None else None,
            "gen_50": rec.gen_50 * rec.min_population / 100 if rec.min_population and rec.gen_50 is not None else None,
            "gen_60": rec.gen_60 * rec.min_population / 100 if rec.min_population and rec.gen_60 is not None else None,
            "gen_70": rec.gen_70 * rec.min_population / 100 if rec.min_population and rec.gen_70 is not None else None,
        }
        for rec in records
    ]

    return response_data

# 성별 인구 데이터 조회 (최대 인구 수)
@router.get("/age_max_population_data", response_model=List[AgeGroupPopulationResponse])
async def get_age_group_max_population_data(
    region_id: str,
    limit: int = 40,  # 한 번에 가져올 데이터 수
    offset: int = 0,   # 시작 위치
    db: AsyncSession = Depends(get_db)
):
    """
    특정 region_id의 연령대별 최대 인구 데이터를 반환
    """
    query = (
        select(PopulationStation)
        .where(PopulationStation.region_id == region_id)
        .order_by(PopulationStation.datetime.desc())  # 최신 데이터 우선 정렬
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(query)
    records = result.scalars().all()
    # 응답 데이터 구성
    response_data = [
        {
            "datetime": rec.datetime.isoformat() if rec.datetime else None,
            "region_id": rec.region_id,
            "gen_10": rec.gen_10 * rec.max_population / 100 if rec.max_population and rec.gen_10 is not None else None,
            "gen_20": rec.gen_20 * rec.max_population / 100 if rec.max_population and rec.gen_20 is not None else None,
            "gen_30": rec.gen_30 * rec.max_population / 100 if rec.max_population and rec.gen_30 is not None else None,
            "gen_40": rec.gen_40 * rec.max_population / 100 if rec.max_population and rec.gen_40 is not None else None,
            "gen_50": rec.gen_50 * rec.max_population / 100 if rec.max_population and rec.gen_50 is not None else None,
            "gen_60": rec.gen_60 * rec.max_population / 100 if rec.max_population and rec.gen_60 is not None else None,
            "gen_70": rec.gen_70 * rec.max_population / 100 if rec.max_population and rec.gen_70 is not None else None,
        }
        for rec in records
    ]

    return response_data