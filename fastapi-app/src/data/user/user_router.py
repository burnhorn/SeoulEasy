from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.database import get_db
from src.data import crud 
from src.schema.user import user_schema
from src.model import model
from starlette import status

router = APIRouter(
    prefix="/user",
)

@router.post("/user", status_code=status.HTTP_204_NO_CONTENT)
async def create_user(user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await crud.get_existing_user(db, user_create=user)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다.")
    db_user = await crud.create_user(db=db, user=user)

@router.get("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    사용자 조회 엔드포인트

    - **user_id**: 조회할 사용자의 ID
    - 사용자가 존재하지 않으면 404 에러를 반환합니다.
    """
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user