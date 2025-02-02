from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
from src.data.database import AsyncSessionLocal, engine, Base, get_db
from src.data import crud 
from src.schema import schemas
from fastapi import HTTPException

# FastAPI 애플리케이션
app = FastAPI()

# 비동기 방식으로 테이블 생성
async def create_tables():
    async with engine.begin() as conn:  # async로 연결
        await conn.run_sync(Base.metadata.create_all)  # 비동기적으로 테이블 생성

@app.post("/user/")
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.create_user(db=db, user=user)  # 비동기 CRUD 호출
    return {"id": db_user.id, "name": db_user.username}

@app.get("/user/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)  # 비동기 CRUD 호출
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# @app.get("/user/verify")
# async def authenticate_user(db: AsyncSession, username: str, password: str):
#     db_user = await crud.get_user(db, username=username)
#     if db_user is None or not crud.verify_password(password, db_user.password):
#         raise HTTPException(status_code=401, detail="Invalid username or password")
#     return db_user