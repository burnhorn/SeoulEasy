from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from src.data.database import engine, Base, get_db, env_activate
from src.data import crud 
from src.schema.user import user_schema
from src.data.user import user_router
from src.data.upload import upload_router
from src.data.population import population_router
# Lifespan 이벤트 임포트 (백그라운드 작업을 위한)
from src.data.population.background_task import background_task  # 백그라운드 작업 가져오기
import asyncio

# svelte 빌드 파일 가져오기 설정
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

import os

if env_activate:
    app = FastAPI()
else:
    # 라이프스팬 이벤트 핸들러 정의
    async def lifespan(app: FastAPI):
        # 애플리케이션 시작 시 실행할 작업(비동기 작업으로 생성하고 실행)
        task = asyncio.create_task(background_task())
        try:
            yield  # 애플리케이션 실행 중...
        finally:
            # 애플리케이션 종료 시 실행할 작업
            task.cancel()
            try:
                await task  # 작업이 안전하게 종료될 때까지 대기
            except asyncio.CancelledError:
                print("백그라운드 작업이 정상적으로 종료되었습니다.")

# FastAPI 애플리케이션(lifespan 이벤트 핸들러 추가)
app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:8000", # Fastapi에 mount하면 fastapi 앱의 주소를 추가
        "https://seouleasy-fastapi-svelte-ebdwarhrbma3hyap.koreacentral-01.azurewebsites.net"
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
app.include_router(population_router.router)

# local 설정
app.mount("/assets", StaticFiles(directory="../svelte-app/dist/assets"))

@app.get("/")
def index():
    return FileResponse("../svelte-app/dist/index.html")

# # azure 설정
# # 현재 파일의 디렉토리 (예: /seoulEasy-app/fastapi-app)
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # Svelte 빌드 결과물 내의 assets 디렉토리 경로 (예: /seoulEasy-app/svelte-app/dist/assets)
# static_assets_dir = os.path.join(current_dir, "../svelte-app/dist/assets")

# # 정적 파일 마운트: 브라우저에서 /assets로 접근하면, 실제 파일은 static_assets_dir에 있음
# app.mount("/assets", StaticFiles(directory=static_assets_dir), name="assets")

# # 루트 엔드포인트: Svelte의 index.html을 제공 (예: /seoulEasy-app/svelte-app/dist/index.html)
# @app.get("/")
# def index():
#     index_path = os.path.join(current_dir, "../svelte-app/dist/index.html")
#     return FileResponse(index_path)
