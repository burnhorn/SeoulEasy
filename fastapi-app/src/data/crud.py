# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.model import model
from src.schema import user_schema
import bcrypt
from fastapi import HTTPException

# 비동기 방식으로 유저 생성
async def create_user(db: AsyncSession, user: user_schema.UserCreate):
    # 비밀번호 해시화
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())  # 비밀번호를 바이트로 변환 후 해시화
    db_user = model.User(username=user.username, password=hashed_password, email=user.email)
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

# 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)