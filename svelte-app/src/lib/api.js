export const _url = import.meta.env.VITE_SERVER_URL.replace(/\/+$/, ''); // URL 끝의 / 제거

export async function getRecommendedPlaces(imageFile) {
    const formData = new FormData();
    formData.append("file", imageFile);

    const response = await fetch(`${_url}/upload/recommend`, {
        method: "POST",
        body: formData,
        mode: "cors", // CORS 요청 모드
    });

    if (!response.ok) {
        throw new Error(`서버 에러: ${response.statusText}`);
    }

    const result = await response.json();
    return result.recommended_places;
}

export async function getPlaceId(place) {
    const encodedPlace = encodeURIComponent(place);
    const response = await fetch(`${_url}/upload/places/${encodedPlace}`, {
        method: "GET",
        mode: "cors", // CORS 요청 모드
    });
    if (!response.ok) {
        throw new Error(`서버 에러: ${response.statusText}`);
    }

    const result = await response.json();
    return result.place_id;
}

// Vision API 호출 함수
export async function analyzeImage(imageFile) {
    const formData = new FormData();
    formData.append("file", imageFile);

    const response = await fetch(`${_url}/vision/analyze`, {
        method: "POST",
        body: formData,
        mode: "cors", // CORS 요청 모드
    });

    if (!response.ok) {
        throw new Error(`Vision API 서버 에러: ${response.statusText}`);
    }

    const result = await response.json();
    return {
        captions: result.captions, // 캡션 데이터
        image: `data:image/jpeg;base64,${result.image}`, // Base64로 인코딩된 이미지
    };
}