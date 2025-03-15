<script>
    let username = "";
    let password = "";
    
  </script>
  
  <main class="container">
    <h2 class="mt-5">로그인</h2>
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
        <label for="password" class="form-label">비밀번호</label>
        <input type="password" class="form-control" username="password" bind:value={password} required />
      </div>
      <button type="submit" class="btn btn-primary">로그인</button>
    </form>
  </main>
  