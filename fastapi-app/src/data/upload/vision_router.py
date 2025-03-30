import os
import base64
import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from fastapi.responses import JSONResponse

# 환경 변수 설정
from dotenv import load_dotenv
from src.data.database import env_activate

if env_activate:
    # Local 환경 설정
    api_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.env'))
    load_dotenv(api_path)
    endpoint = os.getenv('vision_endpoint')
    key = os.getenv('vision_api_key')
else:
    # Azure 환경 설정
    endpoint = os.getenv("vision_endpoint")
    key = os.getenv("vision_api_key")

# Azure Vision API 클라이언트 생성
client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# FastAPI 라우터 생성
router = APIRouter(prefix="/vision", tags=["Vision API"])

# 시각적 특징 설정
visual_features = [
    VisualFeatures.DENSE_CAPTIONS,
]

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Svelte에서 업로드된 이미지를 Azure Vision API로 분석하고 결과를 반환합니다.
    """
    try:
        # 파일 읽기 (바이트 데이터 그대로 사용)
        image_data = await file.read()

        # Azure Vision API 호출 (바이트 데이터를 직접 전달)
        result = client.analyze(
            image_data=image_data,
            visual_features=visual_features,
            gender_neutral_caption=True,  # Optional
            language="en"
        )

        # 분석 결과 처리
        captions = []
        if result.dense_captions is not None:
            for caption in result.dense_captions.list:
                # bounding_box 객체의 속성 확인
                bbox = caption.bounding_box
                # print(dir(bbox))  # 속성 확인용 로그 출력

                # 속성 이름에 따라 값 추출
                captions.append({
                    "text": caption.text,
                    "confidence": caption.confidence,
                    "bounding_box": {
                        "x": bbox.x,
                        "y": bbox.y,
                        "w": bbox.width,
                        "h": bbox.height
                    }
                })

        # 바이트 데이터를 OpenCV에서 처리 가능한 이미지로 디코딩
        image_np = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

        # 이미지에 경계 상자와 캡션 표시
        colors = [
            (255, 0, 0),     # 파란색
            (0, 255, 0),     # 초록색
            (0, 0, 255),     # 빨간색
            (255, 255, 0),   # 청록색
            (255, 0, 255),   # 보라색
            (0, 255, 255)    # 노란색
        ]

        for idx, caption in enumerate(captions):
            bbox = caption["bounding_box"]
            x, y, w, h = int(bbox["x"]), int(bbox["y"]), int(bbox["w"]), int(bbox["h"])
            color = colors[idx % len(colors)]
            cv2.rectangle(image_np, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image_np, f"{caption['text']} ({caption['confidence']:.2f})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # 이미지를 메모리에서 처리
        _, buffer = cv2.imencode('.jpg', image_np)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        # 결과 반환
        return JSONResponse(content={
            "message": "이미지 분석 완료",
            "captions": captions,
            "image": image_base64  # Base64로 인코딩된 이미지
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 분석 중 오류 발생: {str(e)}")