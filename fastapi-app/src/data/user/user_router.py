from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.database import get_db
from src.data import crud 
from src.schema import user_schema

router = APIRouter(
    prefix="/user",
)

@router.get("/{user_id}", response_model=user_schema.UserCreate)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user