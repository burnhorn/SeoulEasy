<script>
    let imageFileInput; // 파일 input 엘리먼트를 바인딩할 변수
    let recommendedPlaces = [];

    let _url = import.meta.env.VITE_SERVER_URL

    async function getRecommendedPlaces() {
        const imageFile = imageFileInput.files[0]; // 선택된 파일 가져오기
        if (!imageFile) {
            alert("이미지를 선택해주세요.");
            return;
        }

        const formData = new FormData();
        formData.append("file", imageFile);

        try {
            const response = await fetch(_url + "/upload/recommend", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`서버 에러: ${response.statusText}`);
            }

            const result = await response.json();
            recommendedPlaces = result.recommended_places;
        } catch (error) {
            console.error("이미지 업로드 오류:", error);
            alert("이미지를 업로드하는 동안 오류가 발생했습니다.");
        }
    }
</script>

<main class="container d-flex justify-content-center align-items-center vh-100">
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
        <button on:click={getRecommendedPlaces} class="btn btn-primary w-100">
            이미지 업로드
        </button>

        {#if recommendedPlaces.length > 0}
            <div class="mt-4">
                <h2 class="h5">추천 관광지:</h2>
                <ul class="list-group mt-2">
                    {#each recommendedPlaces as place}
                        <li class="list-group-item">{place}</li>
                    {/each}
                </ul>
            </div>
        {/if}
    </div>
</main>

<style>
    main {
        background-color: #f8f9fa;
    }

    .card {
        border-radius: 15px;
    }
</style>
