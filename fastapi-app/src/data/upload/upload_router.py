from fastapi import Depends, HTTPException, APIRouter, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.data.database import get_db
from src.data import crud 
from src.schema import user_schema

import os

router = APIRouter(
    prefix="/upload",
)

# 업로드된 파일을 저장할 디렉토리
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # 디렉토리 생성 (이미 존재하면 무시)

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    # 파일 내용을 읽기
    file_content = await file.read()

    # 저장 경로 생성
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # 파일 저장
    with open(file_path, "wb") as f:
        f.write(file_content)

    return {"message": f"이미지 {file.filename} 업로드 성공!", "file_path": file_path}


# 업로드된 파일 저장 디렉토리
UPLOAD_DIR = "video"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # 디렉토리 생성

@router.post("/video")
async def upload_video(file: UploadFile = File(...)):
    # MIME 타입 확인 (동영상만 허용)
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="동영상 파일만 업로드 가능합니다.")

    # 파일 저장 경로 생성
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # 파일 저장
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"message": f"동영상 {file.filename} 업로드 성공!", "file_path": file_path}
