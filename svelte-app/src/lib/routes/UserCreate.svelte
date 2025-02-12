<script>
    let username = "";
    let email = "";
    let password = "";
    let password2 = "";
  
    const handleSubmit = () => {
      // 회원가입 처리 로직
      console.log({ username, email, password, password2 });
    };
  </script>
  
  <main class="container">
    <h2 class="mt-5">회원가입</h2>
    <form on:submit|preventDefault={handleSubmit}>
      <div class="mb-3">
        <label for="username" class="form-label">아이디</label>
        <input
          type="text"
          class="form-control"
          username="username"
          bind:value={username}
          required
          pattern="^[A-Za-z]+$|^[A-Za-z]+[0-9]+$"
          title="영어만 또는 영어와 숫자 조합만 입력 가능합니다."
        />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">이메일</label>
        <input type="email" class="form-control" username="email" bind:value={email} required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">비밀번호</label>
        <input type="password" class="form-control" username="password" bind:value={password} required />
      </div>
      <div class="mb-3">
        <label for="password2" class="form-label">비밀번호 확인</label>
        <input type="password2" class="form-control" username="password2" bind:value={password2} required />
      </div>
      <button type="submit" class="btn btn-primary">회원가입</button>
    </form>
  </main>
  