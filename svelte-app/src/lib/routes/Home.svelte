<script>
    import { onMount } from "svelte";

    let user_info = {}; // 데이터를 저장할 변수 (반응형)

    // FastAPI에서 유저 정보를 가져오는 함수
    async function get_user_info() {
        const response = await fetch("https://seouleasy-fastapi-svelte-ebdwarhrbma3hyap.koreacentral-01.azurewebsites.net/user/1");
        if (response.ok) {
            user_info = await response.json(); // 데이터를 반응형 변수에 저장
        } else {
            console.error("Failed to fetch user info");
        }
    }

    // 컴포넌트가 마운트될 때 데이터 가져오기
    onMount(() => {
        get_user_info();
    });
</script>

<main>
    <h1>Welcome to Home Page</h1>
    <p>This is the home page of our SPA.</p>

    <!-- 데이터 렌더링 -->
    <p>{user_info.username ? `Username: ${user_info.username}` : "Loading..."}</p>
</main>

<style>
    main {
        padding: 20px;
        text-align: center;
    }
</style>
