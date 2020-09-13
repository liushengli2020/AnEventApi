import Vue from 'vue';
import Router from 'vue-router';

import LoginPage from '../components/LoginPage'
import RegisterPage from '../components/RegisterPage'
import EventsPage from '../components/EventList'
import EventSignupPage from "../components/EventSignup"

Vue.use(Router);

export const router = new Router({
  mode: 'history',
  routes: [
    { path: '/', component: EventsPage },
    { path: '/signin', component: LoginPage },
    { path: '/signup', component: RegisterPage },
    { path: '/event-signup', name:'event-signup', component: EventSignupPage },
    // otherwise redirect to home
    { path: '*', redirect: '/' }
  ]
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/', '/signin', '/signup'];
  const authRequired = !publicPages.includes(to.path);
  const user = JSON.parse(localStorage.getItem('user'));

  if (authRequired && !user) {
    return next('/signin');
  }
  else if(user && !user.adminKey && to.path === '/event-signup'){
    return next('/');
  }

  next();
})
