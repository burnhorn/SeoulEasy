<script>
  import { link } from 'svelte-spa-router';

  let isOpen = false; // 토글 상태 관리

</script>

<!-- 네비게이션바 -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
  <div class="container-fluid">
      <a use:link class="navbar-brand" href="/">SeoulEasy</a>
      <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
                <a use:link class="nav-link" href="/user-create">회원가입</a>
            </li>
            <li class="nav-item">
                <a use:link class="nav-link" href="/user-login">로그인</a>
            </li>
            <li class="nav-item">
                <a use:link class="nav-link" href="/uploadImage">이미지 업로드</a>
            </li>
            <li class="nav-item">
                <a use:link class="nav-link" href="/uploadVideo">비디오 업로드</a>
            </li>
          </ul>
      </div>
  </div>
</nav>