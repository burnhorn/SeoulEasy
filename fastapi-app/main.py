from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from src.data.database import engine, Base, get_db
from src.data import crud 
from src.schema import user_schema
from src.data.user import user_router

# FastAPI 애플리케이션
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Svelte 앱의 주소 (필요에 따라 변경)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 비동기 방식으로 테이블 생성
async def create_tables():
    async with engine.begin() as conn:  # async로 연결
        await conn.run_sync(Base.metadata.create_all)  # 비동기적으로 테이블 생성

@app.post("/user/")
async def create_user(user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.create_user(db=db, user=user)  # 비동기 CRUD 호출
    return {"id": db_user.id, "name": db_user.username}

app.include_router(user_router.router)

# @app.get("/user/verify")
# async def authenticate_user(db: AsyncSession, username: str, password: str):
#     db_user = await crud.get_user(db, username=username)
#     if db_user is None or not crud.verify_password(password, db_user.password):
#         raise HTTPException(status_code=401, detail="Invalid username or password")
#     return db_user