# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.model import model
from src.schema.user import user_schema
from passlib.context import CryptContext
from fastapi import HTTPException

# 비동기 방식으로 유저 생성
async def create_user(db: AsyncSession, user: user_schema.UserCreate):
    # 비밀번호 해시화
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated = 'auto')
    # 비밀번호를 바이트로 변환 후 해시화
    db_user = model.User(username=user.username,
                         password=pwd_context.hash(user.password), 
                         email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)  # db_user를 최신 상태로 갱신
    return db_user

# 비동기 방식으로 유저 조회
async def get_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(model.User).filter(model.User.id == user_id))
        return result.scalars().first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# 비동기 방식으로 존재하는 유저 조회
async def get_existing_user(db: AsyncSession, user_create: user_schema.UserCreate):
    try:
        result = await db.execute(
                                select(model.User).filter(
                                    (model.User.username == user_create.username) |
                                    (model.User.email == user_create.email)
                                    )
                                )
        return result.scalars().first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")