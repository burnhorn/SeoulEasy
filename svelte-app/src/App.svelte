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


  const routes = {
    '/': Home,
    '/about': About,
    '/contact': Contact,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
  }

</script>

<Navigation/>

<Header/>

<Router {routes}></Router>

<Footer/>

