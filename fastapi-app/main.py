from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from src.data.database import engine, Base, get_db, env_activate
from src.data import crud 
from src.schema.user import user_schema
from src.data.user import user_router
from src.data.upload import upload_router

# svelte 빌드 파일 가져오기 설정
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

import os

# FastAPI 애플리케이션
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "seouleasy-fastapi-svelte-ebdwarhrbma3hyap.koreacentral-01.azurewebsites.net",
                   ],  # Svelte 앱의 주소 (필요에 따라 변경)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 비동기 방식으로 테이블 생성
async def create_tables():
    async with engine.begin() as conn:  # async로 연결
        await conn.run_sync(Base.metadata.create_all)  # 비동기적으로 테이블 생성

app.include_router(user_router.router)
app.include_router(upload_router.router)

# local 설정
if env_activate:
    app.mount("/assets", StaticFiles(directory="../svelte-app/dist/assets"))

    @app.get("/")
    def index():
        return FileResponse("../svelte-app/dist/index.html")
else:
    # azure 설정
    # 현재 파일의 디렉토리 (예: /seoulEasy-app/fastapi-app)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Svelte 빌드 결과물 내의 assets 디렉토리 경로 (예: /seoulEasy-app/svelte-app/dist/assets)
    static_assets_dir = os.path.join(current_dir, "../svelte-app/dist/assets")

    # 정적 파일 마운트: 브라우저에서 /assets로 접근하면, 실제 파일은 static_assets_dir에 있음
    app.mount("/assets", StaticFiles(directory=static_assets_dir), name="assets")

    # 루트 엔드포인트: Svelte의 index.html을 제공 (예: /seoulEasy-app/svelte-app/dist/index.html)
    @app.get("/")
    def index():
        index_path = os.path.join(current_dir, "../svelte-app/dist/index.html")
        return FileResponse(index_path)
