import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '@/views/movies/Main'
import Login from '@/views/accounts/Login'
import Signup from '@/views/accounts/Signup'
import Profile from '@/views/accounts/Profile'
import Movie from '@/views/movies/Movie'
import Playlist from '@/views/movies/Playlist'
import Detail from '@/views/movies/Detail'
import ReviewDetail from '@/views/movies/ReviewDetail'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main,
  },
  {
    path: '/accounts/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/accounts/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/accounts/profile/:username',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/movies/',
    name: 'Movie',
    component: Movie,
  },
  {
    path: '/movies/playlist',
    name: 'Playlist',
    component: Playlist,
  },
  {
    path: '/movies/detail/:moviePk',
    name: 'Detail',
    component: Detail,
  },
  {
    path: '/movies/commentlist_or_create/:reviewPk',
    name: 'ReviewDetail',
    component: ReviewDetail,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
