# Svelte 빌드 단계
FROM node:18-slim AS svelte-build
WORKDIR /seoulEasy-app/svelte-app
COPY ./svelte-app/package*.json ./
RUN npm install
COPY ./svelte-app ./
RUN npm run build

# 빌드 결과 확인 (디버깅용)
RUN ls -al /seoulEasy-app/svelte-app

# FastAPI 애플리케이션 빌드
FROM python:3.13
WORKDIR /seoulEasy-app/fastapi-app

# 필수 시스템 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    libopenblas-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# pip 최신화 및 requirements 설치
RUN python -m pip install --upgrade pip setuptools wheel
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 애플리케이션 복사 (원본: /seoulEasy-app/fastapi-app 대상: /seoulEasy-app/fastapi-app)
COPY fastapi-app/ ./

# Svelte 빌드 결과 복사 (원본: /seoulEasy-app/svelte-app/dist, 대상: /seoulEasy-app/svelte-app/dist)
COPY --from=svelte-build /seoulEasy-app/svelte-app/dist /seoulEasy-app/svelte-app/dist

# 포트 노출
EXPOSE 8000

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "info"]
