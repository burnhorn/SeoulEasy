from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from src.model.population import PopulationStation
from src.data.database import get_db
from src.schema.population.population_schema import AgeGroupPopulationResponse, GenderPopulationResponse, PopulationRequest, PopulationResponse
import pandas as pd
from sqlalchemy import func

router = APIRouter(prefix = "/populations")

# @router.get("/list", response_model=list[PopulationResponse])
# def get_all_populations(db: Session = Depends(get_db)):
#     """
#     모든 region_id의의 인구 데이터를 반환
#     """
#     db_populations = db.query(PopulationStation).all()
#     return db_populations

# @router.post("/create_population", response_model=PopulationResponse)
# def create_population(population: PopulationRequest, db: Session = Depends(get_db)):
#     """
#     특정 region_id의 인구 데이터를 생성
#     """
#     population_data = service.create_population(population, db)
#     return population_data

@router.get("/region/{region_id}", response_model=list[PopulationResponse])
def get_population_by_region(region_id: int, db: Session = Depends(get_db)):
    """
    특정 region_id의 데이터를 반환
    """
    query = db.query(PopulationStation).filter(PopulationStation.region_id == region_id)
    df = pd.read_sql(query.statement, db.bind)
    return df

@router.get("/get_region_id_time", response_model=list[PopulationResponse])
def get_population_by_region_and_time(
    region_id: int,
    start_time: str,
    end_time: str,
    db: Session = Depends(get_db),
    
):
    """
    특정 region_id와 시간 범위의 데이터를 반환
    """
    query = db.query(PopulationStation).filter(
        PopulationStation.region_id == region_id, 
        func.time(PopulationStation.datetime).between(start_time, end_time))
    df = pd.read_sql(query.statement, db.bind)
    return df

@router.get("/gender_population_data", response_model=List[GenderPopulationResponse])
def get_gender_population_data(
    region_id: int,
    start_time: str,
    end_time: str,
    db: Session = Depends(get_db)
):
    """
    특정 region_id와 시간 범위의 성별 데이터를 반환
    """
    query = db.query(PopulationStation).filter(
        PopulationStation.region_id == region_id, 
        func.time(PopulationStation.datetime).between(start_time, end_time)
    )
    df = pd.read_sql(query.statement, db.bind)
    df["male_min_population"] = df["male_rate"] * df["min_population"] / 100
    df["male_max_population"] = df["male_rate"] * df["max_population"] / 100
    df["female_min_population"] = df["female_rate"] * df["min_population"] / 100
    df["female_max_population"] = df["female_rate"] * df["max_population"] / 100
    gender_df = df[[
        "datetime", "region_id", "male_min_population", "male_max_population",
        "female_min_population", "female_max_population"
    ]]
    return gender_df

@router.get("/age_min_population_data", response_model=List[AgeGroupPopulationResponse])
def get_age_group_min_population_data(
    region_id: int,
    db: Session = Depends(get_db)
):
    """
    특정 region_id의 연령대별 최소 인구 데이터를 반환
    """
    query = db.query(PopulationStation).filter(
        PopulationStation.region_id == region_id
    )
    df = pd.read_sql(query.statement, db.bind)
    for age_group in ["10_gen", "20_gen", "30_gen", "40_gen", "50_gen", "60_gen", "70_gen"]:
        df[age_group] = df[age_group] * df["min_population"] / 100
    rename_columns = {
        "10_gen": "gen_10",
        "20_gen": "gen_20",
        "30_gen": "gen_30",
        "40_gen": "gen_40",
        "50_gen": "gen_50",
        "60_gen": "gen_60",
        "70_gen": "gen_70",
    }
    df.rename(columns=rename_columns, inplace=True)
    age_group_columns = [
        "datetime", "region_id"
    ] + list(rename_columns.values())
    age_group_df = df[age_group_columns]
    return age_group_df

@router.get("/age_max_population_data", response_model=List[AgeGroupPopulationResponse])
def get_age_group_max_population_data(
    region_id: int,
    db: Session = Depends(get_db)
):
    """
    특정 region_id의 연령대별 최대 인구 데이터를 반환
    """
    query = db.query(PopulationStation).filter(
        PopulationStation.region_id == region_id
    )
    df = pd.read_sql(query.statement, db.bind)
    for age_group in ["10_gen", "20_gen", "30_gen", "40_gen", "50_gen", "60_gen", "70_gen"]:
        df[age_group] = df[age_group] * df["max_population"] / 100
    rename_columns = {
        "10_gen": "gen_10",
        "20_gen": "gen_20",
        "30_gen": "gen_30",
        "40_gen": "gen_40",
        "50_gen": "gen_50",
        "60_gen": "gen_60",
        "70_gen": "gen_70",
    }
    df.rename(columns=rename_columns, inplace=True)
    age_group_columns = [
        "datetime", "region_id"
    ] + list(rename_columns.values())
    age_group_df = df[age_group_columns]
    return age_group_df