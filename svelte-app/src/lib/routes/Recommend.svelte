<script>
    import Test from "./test.svelte"; // Test 컴포넌트 임포트
    import { getRecommendedPlaces, getPlaceId, analyzeImage} from "../api.js"; // API 모듈 임포트
    
    let imageFileInput; // 파일 input 엘리먼트를 바인딩할 변수
    let recommendedPlaces = [];
    let selectedPlace = ''; // 선택된 관광지
    let analyzedImage = ""; // 분석된 이미지를 저장할 변수
    let captions = []; // 캡션 데이터를 저장할 변수

    async function handleGetRecommendedPlaces() {
        const imageFile = imageFileInput.files[0]; // 선택된 파일 가져오기
        if (!imageFile) {
            alert("이미지를 선택해주세요.");
            return;
        }

        try {
            // 추천 관광지 가져오기
            recommendedPlaces = await getRecommendedPlaces(imageFile);

            // Vision API 호출
            const result = await analyzeImage(imageFile);
            captions = result.captions; // 캡션 데이터 저장
            analyzedImage = result.image; // Base64 이미지 저장
        } catch (error) {
            console.error("이미지 업로드 오류:", error);
            alert("이미지를 업로드하는 동안 오류가 발생했습니다.");
        }
    }

    async function handleSelectPlace(place) {
        try {
            selectedPlace = await getPlaceId(place);
        } catch (error) {
            console.error("관광지 ID 검색 오류:", error);
            alert("관광지 ID를 검색하는 동안 오류가 발생했습니다.");
        }
    }
</script>

<main class="container d-flex justify-content-center align-items-center">
    <div class="card shadow-lg p-4" style="max-width: 400px; width: 100%;">
        <h1 class="card-title text-center mb-4">이미지 업로드</h1>
        <div class="mb-3">
            <input
                type="file"
                accept="image/*"
                bind:this={imageFileInput}
                class="form-control"
            />
        </div>
        <button on:click={handleGetRecommendedPlaces} class="btn btn-primary w-100">
            이미지 업로드
        </button>

        {#if analyzedImage}
            <div class="mt-4">
                <h2 class="h5">분석된 이미지:</h2>
                <img src={analyzedImage} alt="분석된 이미지" class="img-fluid" />
            </div>
        {/if}

        {#if captions.length > 0}
            <div class="mt-4">
                <h2 class="h5">캡션 데이터:</h2>
                <ul class="list-group mt-2">
                    {#each captions as caption}
                        <li class="list-group-item">
                            {caption.text} (신뢰도: {caption.confidence.toFixed(2)})
                        </li>
                    {/each}
                </ul>
            </div>
        {/if}

        {#if recommendedPlaces.length > 0}
            <div class="mt-4">
                <h2 class="h5">추천 관광지:</h2>
                <ul class="list-group mt-2">
                    {#each recommendedPlaces as place}
                        <li class="list-group-item">
                          <button type="button" class="btn btn-link" on:click={() => handleSelectPlace(place)}>{place}</button>
                        </li>
                    {/each}
                </ul>
            </div>
        {/if}
    </div>
</main>

{#if selectedPlace}
    <Test place={selectedPlace} />
{/if}

<style>
    main {
        background-color: white;
    }

    .card {
        border-radius: 15px;
    }

    .btn-link:hover {
        text-decoration: underline;
    }

    .btn-link {
        text-decoration: none;
        color: inherit;
        padding: 0;
        border: none;
        background: none;
    }

    img {
        max-width: 100%;
        height: auto;
        margin-top: 20px;
    }
</style>