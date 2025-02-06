<script>
    let imageFile; // 사용자가 업로드한 파일을 저장할 변수
    let responseMessage = ""; // 서버 응답 메시지를 저장할 변수

    // 이미지 업로드 함수
    async function uploadImage() {
        if (!imageFile || imageFile.files.length === 0) {
            alert("이미지를 선택해주세요!");
            return;
        }

        const formData = new FormData();
        formData.append("file", imageFile.files[0]); // 파일 객체 추가

        try {
            const response = await fetch("https://seouleasy-fastapi-svelte-ebdwarhrbma3hyap.koreacentral-01.azurewebsites.net/upload/image", {
                method: "POST",
                body: formData,
            });
            const result = await response.json();
            responseMessage = result.message;
        } catch (error) {
            console.error("이미지 업로드 중 에러:", error);
            responseMessage = "이미지 업로드 실패!";
        }
    }
</script>

<main>
    <h1>이미지 업로드</h1>
    <input type="file" accept="image/*" bind:this={imageFile} /> <!-- DOM 요소 바인딩 -->
    <button on:click={uploadImage}>이미지 업로드</button>
    
    {#if responseMessage}
        <p>{responseMessage}</p>
    {/if}
</main>


<style>
    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        padding: 20px;
    }

    input {
        margin-bottom: 10px;
    }

    button {
        padding: 10px 20px;
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    button:hover {
        background-color: #0056b3;
    }

    p {
        margin-top: 10px;
        font-size: 1.2em;
        color: green;
    }
</style>
