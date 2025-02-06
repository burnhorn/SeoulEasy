<script>
    let videoFile; // 업로드할 동영상 파일 변수
    let responseMessage = ""; // 서버 응답 메시지

    async function uploadVideo() {
        if (!videoFile || videoFile.files.length === 0) {
            alert("동영상을 선택해주세요!");
            return;
        }

        const formData = new FormData();
        formData.append("file", videoFile.files[0]); // 파일 객체 추가

        try {
            const response = await fetch("https://seouleasy-fastapi-svelte-ebdwarhrbma3hyap.koreacentral-01.azurewebsites.net/upload/video", {
                method: "POST",
                body: formData,
            });
            const result = await response.json();
            responseMessage = result.message;
        } catch (error) {
            console.error("동영상 업로드 중 에러:", error);
            responseMessage = "동영상 업로드 실패!";
        }
    }
</script>

<main>
    <h1>동영상 업로드</h1>
    <input type="file" accept="video/*" bind:this={videoFile} /> <!-- 동영상 전용 -->
    <button on:click={uploadVideo}>동영상 업로드</button>
    
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
        background-color: #28a745;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    button:hover {
        background-color: #218838;
    }

    p {
        margin-top: 10px;
        font-size: 1.2em;
        color: green;
    }
</style>
