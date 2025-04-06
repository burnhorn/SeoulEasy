# SeoulEasy

**SeoulEasy**는 **OpenAI의 CLIP 모델**과 **Azure Computer Vision** 활용하여 사용자가 업로드한 이미지를 분석하고, **Azure OpenAI GPT-3.5 Turbo**로 해당 이미지와 가장 유사한 관광지를 추천합니다.

- 사용자 이미지 업로드 시, CLIP 모델을 통해 이미지 임베딩과 시각적 유사성을 산출
- Azure AI Vision API로 추출한 이미지 캡션, 주요 요소, 맥락을 설명하는 텍스트 정보를 제공
- 동시에 실시간 데이터와 결합하여 GPT-3.5 Turbo에 전달
    - “이미지와 유사한 이 관광지는 혼잡도가 낮아 방문하기에 적합하다”라는 자연어 기반의 추천 해설을 생성하여 이해할 수 있는 추천 서비스를 구현

**FastAPI**를 백엔드로, **Svelte**를 프론트엔드로 사용하며, 백그라운드 작업을 통해 서울시의 실시간 데이터를 주기적으로 수집하고 API를 통해 추천 관광지의 혼잡도 및 인구 분포도 정보를 제공한 후, 프론트엔드에서 시각화합니다.

---

### 아래의 뱃지를 클릭하면 배포된 프로젝트 사이트로 이동합니다.
[![프로젝트 배포 상태](https://img.shields.io/badge/프로젝트-배포중-brightgreen)](https://seouleasy-fastapi-svelte-ebdwarhrbma3hyap.koreacentral-01.azurewebsites.net/)

---

## 서비스 구조
![Reference Image](https://github.com/burnhorn/SeoulEasy/raw/main/svelte-app/src/assets/images/architecture.svg)

---
## 사용 예시
`이미지를 업로드 하세요!`
![Reference Image](https://github.com/burnhorn/SeoulEasy/raw/main/svelte-app/src/assets/images/recommend1.JPG)

`분위기가 가장 유사한 3곳을 추천합니다!`
![Reference Image](https://github.com/burnhorn/SeoulEasy/raw/main/svelte-app/src/assets/images/recommend2.JPG)

`원하는 곳을 선택하면 현재 (1)혼잡도 (2)혼잡도 설명 (3)실시간 유동인구 분석 차트를 볼 수 있습니다!`
![Reference Image](https://github.com/burnhorn/SeoulEasy/raw/main/svelte-app/src/assets/images/recommend3.JPG)

---

## 주요 기능

1. **실시간 데이터 수집**
    - 백그라운드 작업
        - 서울시의 실시간 도시 데이터를 비동기 작업을 통해 데이터를 주기적으로 수집하고 데이터베이스에 저장합니다.
        - 작업 주기는 5분으로 고정되어 있으며, 작업 처리 시간에 관계없이 일정한 주기를 유지합니다.
   - 데이터는 116개의 특정 지역(`region_id`)별로 저장됩니다.

2. **Clip 모델 기반 이미지 분석 및 추천 기능**
    - 이미지 업로드 및 분석
        - 사용자가 업로드한 이미지를 CLIP 모델을 사용하여 분석합니다.
        - 이미지를 벡터화하여 관광지 설명 텍스트와의 유사도를 계산합니다.
    - 관광지 추천
        - CLIP 모델을 활용하여 이미지와 가장 유사한 관광지 3곳을 추천합니다.
        - 추천된 관광지는 한글로 번역되어 반환됩니다.
    - 파일 유효성 검사
        - 업로드 파일의 MIME 타입, 확장자, 크기 등을 검사하여 유효하지 않은 파일을 차단합니다.

3. **Azure Computer Vision**
    - 사용자가 업로드한 이미지의 캡션, 주요 요소, 맥락을 설명하는 텍스트 정보를 제공합니다.

4. **Azure OpenAI GPT-3.5 Turbo**
    - 추천된 관광지와 해당 실시간 도시 데이터를 GPT-3.5 Turbo에 전달하여 자연어 기반의 추천 해설을 생성합니다.

5. **데이터 시각화**
   - Svelte를 사용하여 데이터를 시각화합니다.
   - Plotly.js를 활용하여 차트를 생성하며, 반응형 디자인을 지원합니다.

---

## 기술 스택

- **AI**: OpenAI의 CLIP 모델, Azure Computer Vision, GPT-3.5 Turbo
- **백엔드**: FastAPI, SQLAlchemy, Azure Database for MySQL
- **프론트엔드**: Svelte, Plotly.js
- **비동기 작업**: Python `asyncio`, `httpx`
- **API 데이터 소스**: 서울시 공공데이터 API

---

## 설치 및 실행

### 1. 프로젝트 클론

```bash
git clone https://github.com/your-repo/seoulEasy-app.git
cd seoulEasy-app
```

### 2. 백엔드 설정

#### 1. Python 가상환경 생성 및 활성화
- Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```
- Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### 2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

#### 3. 환경 변수 설정
- 로컬 작업을 위한 fastapi 프로젝트 루트의 상위 루트에 .env 파일을 생성하고 다음 내용을 추가합니다:
```bash
SQLALCHEMY_DATABASE_URL = your_SQLALCHEMY_DATABASE_URL
SECRET_KEY = your_SECRET_KEY_for_password
API_KEY = your_seoul_api_key
```

- fastapi-app/src/data/database에서 데이터베이스 및 환경변수 지정하기
```bash
sqlite_test = False # False: azure mysql 사용 / True: 로컬의 sqlite 사용
env_activate = False # False: azure 환경변수 사용 / True: 로컬의 .env 환경변수 사용

# # 로컬 작업 시
app = FastAPI()

# # azure 배포 시
# 라이프스팬 이벤트 핸들러 정의하기
async def lifespan(app: FastAPI):
```

- svelte의 fetch url 설정을 위해 svelte 프로젝트 루트에 .env 파일을 생성하고 다음 내용을 추가합니다:
```bash
VITE_SERVER_URL= your_WEBSITE_URL   # 배포 서버 작업 시
# VITE_SERVER_URL=http://127.0.0.1:8000  # 로컬 서버 작업시

```
#### 4. 백엔드 실행
```bash
uvicorn main:app --reload
```

### 3. 프론트엔드 설정
#### 1. 프론트엔드 디렉토리로 이동
```bash
cd svelte-app
```

#### 2. 필요한 패키지 설치
```bash
npm install
```

#### 3. 프론트엔드 실행
```bash
npm run dev
```

---

## 구성 요소 상세 설명
### 1. 백엔드
1. **API 엔드포인트**
    - /region/{region_id}:
        - 특정 지역의 데이터를 페이징하여 반환합니다.
        - 최신 데이터를 우선 정렬하며, 기본적으로 40개의 데이터를 반환합니다.

2. **백그라운드 작업**
    - background_task 함수:
        - 5분 간격으로 데이터를 수집합니다.
        - 작업 시작 시점을 고정하여 API 데이터 갱신 주기와 동기화합니다.
```python
async def background_task():
    while True:
        now = datetime.now()
        next_start_time = (now + timedelta(seconds=TASK_INTERVAL)).replace(second=0, microsecond=0)
        if next_start_time.second != 0:
            next_start_time += timedelta(minutes=1)
        start_time = time.time()
        for i in range(0, len(AREA_NM_LIST), BATCH_SIZE):
            batch = AREA_NM_LIST[i:i + BATCH_SIZE]
            batch_tasks = [fetch_population_data(area_name) for area_name in batch]
            await asyncio.gather(*batch_tasks)
        end_time = time.time()
        now = datetime.now()
        wait_time = (next_start_time - now).total_seconds()
        if wait_time > 0:
            await asyncio.sleep(wait_time)
```
3. **모델 지정, 이미지 업로드, 추천**
- 개요
    - URL: /upload/recommend
    - 메서드: POST
    - 설명: 사용자가 업로드한 이미지를 분석하여 관광지를 추천합니다.
- 주요 특징
    - CLIP 모델 활용
        - 이미지와 텍스트 간의 유사도를 계산하여 정확한 추천 결과 제공.
    - 유연한 확장성
        - 관광지 설명 텍스트를 추가하거나 수정하여 추천 결과를 쉽게 조정 가능.
    - GPU 최적화
        - GPU를 활용 가능 시 선택적 활용하여 이미지 처리 속도를 향상.
    - 파일 유효성 검사
        - 업로드된 파일의 형식과 크기를 철저히 검사하여 안정성 확보.

```python
## CLIP 모델 활용, 이미지 처리 및 추천
# 업로드된 이미지를 CLIP 모델로 벡터화한 후, 관광지 설명 텍스트와의 유사도를 계산합니다.
def recommend_places(image_features_np):
    place_inputs = processor(text=place_descriptions, return_tensors="pt", padding=True)
    for key in place_inputs:
        place_inputs[key] = place_inputs[key].to(device)
    place_features = model.get_text_features(**place_inputs)
    place_features_np = place_features.cpu().detach().numpy()

    similarities = cosine_similarity(image_features_np, place_features_np)
    top_indices = np.argsort(similarities[0])[::-1][:3]
    recommended_places = [place_descriptions[i] for i in top_indices]
    translated_places = translate_to_korean(recommended_places, place_name_mapping)
    return translated_places

## 유연한 확장성: 관광지 데이터
# 관광지 설명 텍스트는 CLIP 모델의 텍스트 임베딩 생성에 사용됩니다.
place_descriptions = [
    "Gangnam MICE Special Tourist Zone, a modern business and convention district in Seoul...",
    "Dongdaemun Fashion Town Special Tourist Zone, a global fashion hub in Seoul...",
    ...
]

## 추천된 관광지는 한글명으로 반환
def translate_to_korean(recommended_places, place_name_mapping):
    translated_places = []
    for place in recommended_places:
        korean_name = place_name_mapping.get(place, place)
        translated_places.append(korean_name)
    return translated_places
```

4. **데이터베이스 모델**
    - PopulationStation:
        - 지역 ID, 혼잡도, 성별 비율, 세대별 비율, 최소/최대 인구수 등을 저장합니다.


### 2. 프론트엔드
1. **주요 컴포넌트**
    - App.svelte:
        - 전체 애플리케이션의 라우팅 및 레이아웃을 관리합니다.
    - Recommend.svelte:
        - 사용자가 이미지를 업로드한 후, 원하는 관광지를 선택하면 해당 지역의 데이터를 시각화하는 test.svelte 페이지로 이동합니다.
    - test.svelte:
        - 특정 지역의 데이터를 시각화하는 페이지로, Plotly.js를 사용하여 차트를 생성합니다.

2. **차트 시각화**
   - updateCharts 함수:
        - Plotly.js를 사용하여 데이터를 시각화합니다.
        - x축은 datetime 값을 기준으로 표시되며, y축은 다양한 데이터(혼잡도, 성별 비율 등)를 표시합니다.

```javascript
function updateCharts() {
  const dates = regionData.map(d => d.datetime);
  const leftChartData = [
    { x: dates, y: regionData.map(d => d.male_rate), type: 'scatter', mode: 'lines+markers', name: 'Male Rate' },
    { x: dates, y: regionData.map(d => d.female_rate), type: 'scatter', mode: 'lines+markers', name: 'Female Rate' }
  ];
  Plotly.newPlot('left-chart', leftChartData, {
    title: 'Male vs Female Rate',
    xaxis: { title: 'Time', type: 'date', tickformat: '%H:%M:%S' },
    yaxis: { title: 'Rate (%)' },
    responsive: true
  });
}
```

---

## 라이선스
### 이 프로젝트는 「저작권법」 제24조의2(공공저작물의 자유이용) 하에 배포됩니다. 
![Reference Image](https://www.seoul.go.kr/res_newseoul/images/common/img_opentype01-big.jpg)


1. **본 프로젝트는 서울시 데이터를 활용한 서울시민을 위한 편리한 개인 서비스로서 서울특별시와 전혀 연관이 없습니다.**
2. **본 저작물은 '서울특별시'에서 공공누리 제1유형으로 개방한 '서울시 실시간 도시데이터(서울특별시)'을 이용하였습니다.**
3. **해당 저작물은 '서울특별시, https://data.seoul.go.kr/dataList/OA-21285/F/1/datasetView.do' 에서 무료로 다운받으실 수 있습니다.**
