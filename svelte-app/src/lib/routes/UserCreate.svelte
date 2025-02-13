<script>
    import Home from "./Home.svelte";
    
    let _url = import.meta.env.VITE_SERVER_URL

    let username = "";
    let email = "";
    let password = "";
    let password2 = "";
  
    let responseMessage = [];

    const handleSubmit = () => {
      // 회원가입 처리 로직
      console.log({ username, email, password, password2 });
    };

    async function createUser() {
      if (!username || !email || !password || !password2) {
        alert("모든 입력을 해주세요!");
        return;
      }

      let params = {
            username: username,
            password: password,
            password2: password2,
            email: email
        };

      try {
        const response = await fetch(_url + "/user/user", {
                                    method: "POST", // 필요한 경우 적절한 HTTP 메소드 지정
                                    headers: {
                                      "Content-Type": "application/json",
                                    },
                                    body: JSON.stringify(params), // params는 전송할 데이터 객체
                                  });

      if (response.status !== 204) {
        const result = await response.json();
        console.log(result);
      } else {
        console.log("회원 가입이 성공했습니다.");
      }
    } catch (error) {
      console.error("회원 가입 중 에러:", error);
    }
  }

</script>
  
  <main class="container">
    <h2 class="mt-5">회원가입</h2>
    <form method="post" on:submit|preventDefault={createUser}>
      <div class="mb-3">
        <label for="username" class="form-label">아이디</label>
        <input
          type="text"
          class="form-control"
          name="username"
          bind:value={username}
          required
          pattern="^[A-Za-z]+$|^[A-Za-z]+[0-9]+$"
          title="영어만 또는 영어와 숫자 조합만 입력 가능합니다."
        />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">이메일</label>
        <input type="email" class="form-control" name="email" bind:value={email} required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">비밀번호</label>
        <input type="password" class="form-control" name="password" bind:value={password} required />
      </div>
      <div class="mb-3">
        <label for="password2" class="form-label">비밀번호 확인</label>
        <input type="password" class="form-control" name="password2" bind:value={password2} required />
      </div>
      <button type="submit" class="btn btn-primary">회원가입</button>
    </form>
  </main>
  