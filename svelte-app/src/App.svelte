<script>
  import Router, { link } from 'svelte-spa-router';
  import Footer from './lib/components/Footer.svelte';
  import Header from './lib/components/Header.svelte';
  import Navigation from './lib/components/Navigation.svelte';
  import Home from './lib/routes/Home.svelte';
  import About from './lib/routes/About.svelte';
  import Contact from './lib/routes/Contact.svelte';
  import UserCreate from './lib/routes/UserCreate.svelte';
  import UserLogin from './lib/routes/UserLogin.svelte';
  import UploadImage from './lib/routes/UploadImage.svelte';
  import UploadVideo from './lib/routes/UploadVideo.svelte';
  import Recommend from './lib/routes/Recommend.svelte';
  import Test from './lib/routes/test.svelte';
  

  const routes = {
    // '/': Home,
    '/' : Recommend,
    '/test' : Test,
    '/about': About,
    '/contact': Contact,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/uploadImage': UploadImage,
    '/uploadvideo': UploadVideo
  }

</script>

<Navigation/>

<Header/>

<div class="content">
  <Router {routes}></Router>
</div>


<Footer />


<style>
  .content {
    padding-bottom: 100px; /* 콘텐츠와 Footer 간 여백 */
  }
  
</style>