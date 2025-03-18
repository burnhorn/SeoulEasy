export const _url = import.meta.env.VITE_SERVER_URL;

export async function getRecommendedPlaces(imageFile) {
    const formData = new FormData();
    formData.append("file", imageFile);

    const response = await fetch(`${_url}/upload/recommend`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error(`서버 에러: ${response.statusText}`);
    }

    const result = await response.json();
    return result.recommended_places;
}

export async function getPlaceId(place) {
    // URL 인코딩을 올바르게 처리
    const encodedPlace = encodeURIComponent(place);
    const response = await fetch(`${_url}/upload/places/${encodedPlace}`);
    if (!response.ok) {
        throw new Error(`서버 에러: ${response.statusText}`);
    }

    const result = await response.json();
    return result.place_id;
}