from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.database import get_db
from src.data import crud 
from src.schema import user_schema

router = APIRouter(
    prefix="/user",
)

@router.post("/user/")
async def create_user(user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.create_user(db=db, user=user)  # 비동기 CRUD 호출
    return {"id": db_user.id, "name": db_user.username}

@router.get("/{user_id}", response_model=user_schema.UserCreate)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# @app.get("/user/verify")
# async def authenticate_user(db: AsyncSession, username: str, password: str):
#     db_user = await crud.get_user(db, username=username)
#     if db_user is None or not crud.verify_password(password, db_user.password):
#         raise HTTPException(status_code=401, detail="Invalid username or password")
#     return db_user