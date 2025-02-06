from fastapi import Depends, HTTPException, APIRouter, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from src.data.database import get_db
from src.data import crud 
from src.schema import user_schema

import os

router = APIRouter(
    prefix="/upload",
)

# CLIP 모델 로드
# 저장 경로 설정 (azure의 작업폴더(/fastapi-app)에 맞춰서 경로 설정을 해줘야 한다.)
MODEL_DIR = "./src/clip_model"
UPLOAD_DIR = "upload_recommand"

# 모델 로드 함수
def load_or_download_model(model_dir):
    if not os.path.exists(model_dir):
        os.makedirs(model_dir, exist_ok=True)
        print("모델이 로컬에 없습니다. 다운로드 중...")
        # 모델과 프로세서 다운로드 및 저장
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        model.save_pretrained(model_dir)
        processor.save_pretrained(model_dir)
        print("모델이 성공적으로 저장되었습니다.")
    else:
        print("로컬에서 모델을 불러옵니다.")

    # 로컬에서 모델과 프로세서 로드
    model = CLIPModel.from_pretrained(model_dir)
    processor = CLIPProcessor.from_pretrained(model_dir)
    return model, processor

# 모델 및 프로세서 로드
model, processor = load_or_download_model(MODEL_DIR)

# 업로드 디렉토리 생성
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/recommend")
async def upload_image(file: UploadFile = File(...)):
    # 이미지 저장
    file_content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file_content)

    # 이미지 처리
    image = Image.open(file_path)
    inputs = processor(images=image, return_tensors="pt")
    image_features = model.get_image_features(**inputs)

    # 관광지 추천 로직 
    recommended_places = recommend_places(image_features)
    
    return {"message": "이미지 업로드 및 분석 완료", "recommended_places": recommended_places}

def recommend_places(image_features):
    # 예시로 관광지 설명 텍스트를 벡터화
    place_descriptions = [
    "Gangnam MICE Special Tourist Zone, a modern business and convention district in Seoul, featuring COEX, luxury shopping malls, and vibrant nightlife",
    "Dongdaemun Fashion Town Special Tourist Zone, a global fashion hub in Seoul, home to DDP, 24-hour shopping malls, and street markets with the latest trends",
    "Myeong-dong Namdaemun Bukchang-dong Da-dong Mugyo-dong Special Tourist Zone, a major shopping district in Seoul, famous for beauty stores, street food, and Namdaemun Market",
    "Itaewon Special Tourist Zone, a multicultural hotspot in Seoul, known for international restaurants, foreign-friendly shops, and a diverse nightlife scene",
    "Jamsil Special Tourist Zone, a family-friendly entertainment district in Seoul, featuring Lotte World Theme Park, Lotte Tower, and Seokchon Lake",
    "Jongno Cheonggye Special Tourist Zone, a historical and cultural area in Seoul, featuring traditional markets, Cheonggyecheon Stream, and heritage sites",
    "HongDae Culture & Arts Special Tourist Zone, a youthful and artistic district in Seoul, known for indie music, street performances, and trendy fashion stores",
    "Gyeongbokgung Palace, the largest and most iconic Joseon-era palace in Seoul, featuring traditional Korean architecture and the Royal Guard Changing Ceremony",
    "Gwanghwamun & Deoksugung Palace, a historical area in Seoul, featuring Gwanghwamun Square, Deoksugung Palace, and the Changing of the Royal Guard",
    "Bosingak, a historic bell pavilion in Seoul, famous for its New Year's Eve bell-ringing ceremony",
    "Amsa Prehistoric Settlement Site, an ancient archaeological site in Seoul, showcasing Neolithic artifacts and pit houses",
    "Changdeokgung Palace & Jongmyo Shrine, a UNESCO World Heritage site in Seoul, featuring a beautifully preserved Joseon-era palace and a royal ancestral shrine",
    "Gasan Digital Complex Station, a major transportation hub in Seoul, located near tech business districts and outlet shopping malls",
    "Gangnam Station, a bustling commercial and nightlife area in Seoul, known for shopping streets, restaurants, and entertainment venues",
    "Konkuk University Station, a lively district in Seoul, featuring Star City Mall, Ttukseom Hangang Park, and vibrant student culture",
    "Godeok Station, a gateway to the residential district of Godeok in Seoul, with nearby parks and modern urban developments",
    "Express Bus Terminal Station, a major transit hub in Seoul, connected to shopping malls, express bus services, and underground markets",
    "Seoul National University of Education Station, a transit point in Seoul, near educational institutions and business districts",
    "Guro Digital Complex Station, a key transportation hub in Seoul, located in a major IT and tech business district",
     "Guro Station, a major transit hub in Seoul, located near shopping areas and the Guro Industrial Complex",
    "Gunja Station, a key transfer station in Seoul, providing access to nearby residential and commercial districts",
    "Namguro Station, a local transit point in Seoul, serving the Guro district and surrounding neighborhoods",
    "Daerim Station, a bustling area in Seoul, known for its vibrant Chinese-Korean community and authentic cuisine",
    "Dongdaemun Station, a gateway to Dongdaemun Market in Seoul, surrounded by fashion malls and historical landmarks",
    "Ttukseom Station, an access point to Ttukseom Hangang Park in Seoul, popular for outdoor activities and cultural events",
    "Miasageori Station, a transit station in northern Seoul, providing access to shopping centers and residential areas",
    "Balsan Station, a transport hub in western Seoul, located near Magok Industrial Complex and local business districts",
    "Bukhansan Ui Station, a starting point for hiking trails in Bukhansan National Park, offering scenic mountain views",
    "Sadang Station, a busy transfer station in Seoul, connecting commuters to southern districts and major transit lines",
     "Samgakji Station, a historical transit point in Seoul, located near the War Memorial of Korea and Yongsan district",
    "Seoul National University Station, the main access point to Seoul National University, surrounded by student-friendly shops and cafes",
    "Seoul Botanic Park·Magongnaru Station, a gateway to Seoul Botanic Park, featuring themed greenhouses and ecological gardens",
    "Seoul Station, a major transportation hub in Seoul, connecting KTX, subways, and an extensive shopping and business district",
    "Seolleung Station, a historical and business area in Seoul, home to Seolleung and Jeongneung Royal Tombs, a UNESCO World Heritage site",
    "Sungshin Women's University Station, a lively student district in Seoul, featuring shopping streets, cafes, and a vibrant university atmosphere",
    "Suyu Station, a transit station in northern Seoul, located near traditional markets and hiking trails leading to Bukhansan National Park",
    "Sinnonhyeon·Nonhyeon Station, a bustling commercial district in Seoul, known for nightlife, restaurants, and modern entertainment venues",
    "Sindorim Station, a key transfer station in Seoul, connecting subway lines and adjacent to D-Cube City shopping mall and cultural spaces",
    "Sillim Station, a busy commercial and residential area in Seoul, known for its dynamic food scene and startup-friendly business environment",
    "Sinchon·Ewha Womans University Station, a youthful district in Seoul, famous for Ewha Womans University, Sinchon shopping streets, and student culture",
    "Yangjae Station, a business and tech hub in Seoul, close to Yangjae Citizen’s Forest and major corporate offices",
    "Yeoksam Station, a central business district in Seoul, home to major IT companies, co-working spaces, and premium dining options",
    "Yeonsinnae Station, a suburban area in northern Seoul, offering access to Dobongsan and Bukhansan hiking trails",
    "Omokgyo·Mok-dong Stadium Station, a family-friendly area in Seoul, featuring Mok-dong Ice Rink, sports facilities, and shopping centers",
    "Wangsimni Station, a major transit hub in Seoul, connected to Wangsimni Square, shopping complexes, and cultural attractions",
    "Yongsan Station, a key railway and KTX station in Seoul, home to Yongsan Electronics Market and large shopping complexes",
    "Itaewon Station, the heart of Itaewon, known for its multicultural restaurants, nightlife, and vibrant expat community",
    "Jangji Station, a residential district in southeastern Seoul, offering convenient access to shopping centers and local parks",
    "Janghanpyeong Station, an area in eastern Seoul known for its used car market and proximity to Cheonggyecheon Stream",
    "Cheonho Station, a busy commercial district in Seoul, located near department stores, entertainment venues, and Han River parks",
    "Chongshin University(Isu) Station, a busy transfer station in Seoul, located near Chongshin University and local dining areas",
    "Chungjeongno Station, a historical and business district in Seoul, providing access to cultural sites and government buildings",
    "Hapjeong Station, a vibrant area in Seoul, known for trendy cafes, indie music venues, and access to Hongdae and Mangwon districts",
    "Hyehwa Station, a cultural hotspot in Seoul, famous for Daehangno, small theaters, and street performances",
    "Hongik University Station(Line 2), the gateway to Hongdae, Seoul’s youthful hub for art, nightlife, and indie music culture",
    "Hoegi Station, a student-friendly area in Seoul, located near Kyung Hee University and traditional food markets",
    "4·19 Cafe Street, a charming street in northern Seoul, lined with cafes and offering scenic views of Bukhansan Mountain",
    "Garak Market, one of Seoul’s largest wholesale food markets, known for fresh seafood, meat, and produce",
    "Garosu-gil, a trendy street in Seoul’s Gangnam district, famous for boutique shops, stylish cafes, and art galleries",
    "Gwangjang(Traditional) Market, one of Seoul’s oldest markets, offering authentic Korean street food like bindaetteok and gimbap",
    "Gimpo Airport, a major airport in Seoul serving domestic and international flights, connected to the city’s subway network",
    "Naksan Park·Ihwa Village, a scenic area in Seoul featuring old city walls, street art, and panoramic night views",
    "Noryangjin, a famous seafood market district in Seoul, known for its fresh fish auctions and raw seafood restaurants",
    "Deoksugung-gil·Jeongdong-gil, a historic walking street in Seoul, lined with royal palaces, museums, and European-style architecture",
    "Bangbae Food Alley, a hidden gem in Seoul’s Bangbae district, offering a variety of local Korean restaurants and street food",
    "Bukchon Hanok Village, a picturesque neighborhood in Seoul, preserving traditional Korean hanok houses and cultural heritage",
    "Seochon, a historic and artistic district in Seoul, located near Gyeongbokgung Palace and known for its traditional cafes and shops",
    "Seongsu Cafe Street, a hipster-friendly area in Seoul, featuring industrial-style cafes, artisan bakeries, and creative spaces",
    "Suyuri Food Alley, a local food district in northern Seoul, famous for its affordable Korean barbecue and traditional dishes",
    "Ssangmun-dong Restaurant Street, a hidden gem in northern Seoul, known for its diverse local eateries and traditional Korean dishes",
    "Apgujeong Rodeo Street, a luxury shopping district in Seoul, featuring high-end fashion brands, stylish cafes, and entertainment venues",
    "Yeouido, Seoul’s financial district, home to major banks, skyscrapers, and the scenic Yeouido Hangang Park",
    "Yeonnam-dong, a trendy neighborhood in Seoul, famous for its artistic vibe, indie cafes, and Gyeongui Line Forest Park",
    "Yeongdeungpo Time Square, a major shopping and entertainment complex in Seoul, offering luxury stores, cinemas, and fine dining",
    "Hankuk University of Foreign Studies, a global education hub in Seoul, surrounded by international restaurants and student-friendly cafes",
    "Yongnidan-gil, a rising hotspot in Seoul’s Yongsan district, known for its unique fusion restaurants, small bars, and trendy cafes",
    "Itaewon Antiques Street, a charming area in Seoul, featuring vintage furniture shops, unique collectibles, and a historic international atmosphere",
    "Insa-dong, a cultural and artistic district in Seoul, famous for traditional Korean tea houses, art galleries, and souvenir shops",
    "Changdong New Economic Center, a developing business hub in northern Seoul, focusing on tech startups and cultural innovation",
    "Cheongdam-dong Luxury Fashion Street, a high-end shopping district in Seoul, home to global designer boutiques and flagship stores",
    "Traditional Market in Cheongnyangni Jegi-dong, a bustling market in Seoul, offering fresh produce, herbal medicine, and street food",
    "Haebangchon·Gyeongnidan-gil, a multicultural neighborhood in Seoul, known for international cuisine, indie cafes, and a vibrant expat community",
    "DDP (Dongdaemun Design Plaza), an iconic modern landmark in Seoul, hosting exhibitions, fashion events, and futuristic architecture",
    "DMC (Digital Media City), a high-tech business district in Seoul, featuring media companies, futuristic buildings, and digital innovation centers",
    "Gangseo Hangang Park, a riverside park in western Seoul, popular for cycling, picnics, and scenic sunset views along the Han River",
    "Gocheok Dome, South Korea’s first domed baseball stadium, hosting major sports events, concerts, and KBO League games",
    "Gwangnaru Hangang Park, a nature-friendly park along the Han River, offering watersports, bike trails, and eco-friendly landscapes",
    "Gwanghwamun Square, a historic plaza in central Seoul, featuring statues of King Sejong and Admiral Yi Sun-sin, with cultural landmarks nearby",
    "The National Museum of Korea·Yongsan Family Park, a major museum in Seoul showcasing Korea’s rich history, located next to a peaceful urban park",
    "Nanji Hangang Park, an eco-friendly riverside park in Seoul, known for its vast camping sites, bike trails, and music festivals",
    "Namsan Park, a scenic urban park in central Seoul, home to N Seoul Tower and offering panoramic views of the city",
    "Nodeul Island, a cultural and arts space on the Han River, featuring music performances, cafes, and creative studios",
    "Ttukseom Hangang Park, a vibrant riverside park in Seoul, popular for water sports, picnics, and seasonal festivals",
    "Mangwon Hangang Park, a local favorite for cycling, jogging, and enjoying peaceful riverside landscapes in western Seoul",
    "Banpo Hangang Park, famous for the Banpo Rainbow Fountain and scenic night views of Seoul's skyline along the Han River",
    "Dream Forest, one of the largest parks in northern Seoul, featuring walking trails, an observatory, and cultural spaces",
    "Bulgwangcheon River, a picturesque urban stream in Seoul, lined with walking paths, bike lanes, and cherry blossoms in spring",
    "Seoripul Park·Montmartre Park, a pair of serene parks in Seoul, offering scenic walking trails and a Parisian-inspired atmosphere",
    "Seoul Plaza, a central gathering space in front of City Hall, hosting seasonal events, ice skating, and public performances",
    "Seoul Grand Park, a massive recreational complex in Gwacheon, featuring a zoo, botanical garden, and amusement park",
    "Seoul Forest, a large eco-friendly park in Seoul, offering deer feeding, bike trails, and scenic picnic spots",
    "Achasan, a small but scenic mountain in eastern Seoul, popular for sunrise hikes and panoramic city views",
    "Yanghwa Hangang Park, a peaceful riverside park in western Seoul, known for its flower gardens and riverside walking paths",
    "Children's Grand Park, a family-friendly park in Seoul with a zoo, botanical garden, and playgrounds",
    "Yeouido Hangang Park, a popular riverside park in Seoul, famous for cherry blossom festivals and stunning sunset views",
    "World Cup Park, an eco-park in western Seoul, created on a former landfill site, featuring Haneul Park and migratory bird habitats",
    "Eungbongsan, a small mountain in Seoul, known for its fortress ruins and stunning views of the Han River",
    "Ichon Hangang Park, a tranquil riverside park in Seoul, featuring open green spaces, bike paths, and cultural sculptures",
    "Jamsil (Seoul) Sports Complex, a major sports venue in Seoul, hosting international events, concerts, and baseball games",
    "Jamsil Hangang Park, a scenic riverside park in eastern Seoul, offering waterfront leisure facilities and sports grounds",
    "Jamwon Hangang Park, a peaceful section of the Han River parks, popular for yoga, jogging, and riverside relaxation",
    "Cheonggyesan, a natural mountain near Seoul, known for its well-maintained hiking trails and lush forests",
    "Cheongwadae, the former presidential residence of South Korea, now open to the public for cultural tours and historical exhibitions",
    "Bukchang-dong Food Alley, a hidden gem in Seoul’s business district, famous for traditional Korean BBQ and seafood restaurants",
    "Namdaemun Market, Korea’s largest traditional market, offering street food, souvenirs, and wholesale goods",
    "Ikseon-dong, a charming neighborhood in Seoul, featuring narrow alleys lined with hanok-style cafes, boutique shops, and restaurants",
]

    # 관광지 텍스트 임베딩 생성
    place_inputs = processor(text=place_descriptions, return_tensors="pt", padding=True)
    place_features = model.get_text_features(**place_inputs)
    
    # 이미지와 텍스트 벡터 간의 유사도 계산
    similarities = cosine_similarity(image_features.detach().numpy(), place_features.detach().numpy())
    
     # 유사도를 정렬하고 상위 3개의 인덱스 가져오기
    top_indices = np.argsort(similarities[0])[::-1][:3]  # 유사도를 내림차순으로 정렬 후 상위 3개 선택
    
    # 상위 3개의 관광지 반환
    recommended_places = [place_descriptions[i] for i in top_indices]
    return recommended_places


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
