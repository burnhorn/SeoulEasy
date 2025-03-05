from datetime import timedelta, datetime, timezone

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.database import get_db
from src.data import crud 
from src.schema.user import user_schema
from src.model import model
from starlette import status

# 로그인 구현을 위한 라이브러리
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import os
from dotenv import load_dotenv

router = APIRouter(
    prefix="/user",
)

secret_key_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '.env'))

# .env 파일을 로드합니다.
load_dotenv(secret_key_env_path)
print(secret_key_env_path)
# 환경 변수를 가져옵니다.
SECRET_KEY_ENV = os.getenv('SECRET_KEY')

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = SECRET_KEY_ENV
ALGORITHM = "HS256"


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
async def create_user(user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await crud.get_existing_user(db, user_create=user)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다.")
    db_user = await crud.create_user(db=db, user=user)

@router.get("/id/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    사용자 조회 엔드포인트
    - 비밀번호가 있기 때문에 HTTP 204로 반환
    - **user_id**: 조회할 사용자의 ID
    - 사용자가 존재하지 않으면 404 에러를 반환합니다.
    """
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return 

@router.get("/username/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def read_username(username: str, db: AsyncSession = Depends(get_db)):
    """
    사용자 조회 엔드포인트
    - 비밀번호가 있기 때문에 HTTP 204로 반환
    - **username**: 조회할 사용자의 username
    - 사용자가 존재하지 않으면 404 에러를 반환합니다.
    """
    db_user = await crud.get_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return 

@router.post("/login", response_model=user_schema.Token)
async def login_with_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                  db: AsyncSession = Depends(get_db)):
    
    user = await crud.get_username(db, form_data.username)
    if not user or not crud.pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    data = {
        "sub": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }