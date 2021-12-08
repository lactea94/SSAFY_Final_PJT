import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import router from '@/router'

Vue.use(Vuex)

import axios from 'axios'
import Swal from 'sweetalert2'

export default new Vuex.Store({
  plugins: [
    createPersistedState(),
  ],
  state: {
    authToken: localStorage.getItem('jwt'),
    movies: [],
    myUsername: '',
    recommends: [],
  },
  mutations: {
    SET_AUTH_TOKEN: function (state, token) {
      state.authToken = token
      localStorage.setItem('jwt', token)
    },
    DELETE_AUTH_TOKEN: function (state) {
      localStorage.removeItem('jwt')
      state.authToken = null
    },
    GET_MOVIE_DATA: function (state, result) {
      state.movies = result
    },
    SET_MY_USERNAME: function (state, userName) {
      state.myUsername = userName
    },
    DELETE_MY_USERNAME: function(state) {
      state.myUsername = ''
    },
    GET_RECOMMEND_DATA: function (state, result) {
      state.recommends = result
    },
  },
  getters: {
    isLogin: function (state) {
      return state.authToken ? true : false 
    }
  },
  actions: {
    login: function ({ commit }, credentials) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/api-token-auth/',
        data: credentials,
      })
        .then(res => {
          console.log(res.config.data.split('"')[3])
          commit('SET_MY_USERNAME', res.config.data.split('"')[3])
          commit('SET_AUTH_TOKEN', res.data.token)
          Swal.fire({
            position: 'top-end',
            icon: 'success',
            title: 'Welcome!',
            showConfirmButton: false,
            timer: 1500,
          })
          router.push({ name: 'Profile', params:{ username: res.config.data.split('"')[3] }})
        })
        .catch(err => {
          console.log(err)
        })
    },
    logout: function ({ commit }) {
      commit('DELETE_AUTH_TOKEN')
      commit('DELETE_MY_USERNAME')
      router.push({ name: 'Login' })
    },
    signup: function (context, credentials) {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/signup/',
        data: credentials,
      })
        .then((res) => {
          console.log(res)
          this.dispatch('login', credentials)
        })
        .catch(err => {
          console.log(err)
          Swal.fire({
            icon: 'error',
            title: 'Stop!',
            text: '등록된 이름입니다!.',
          })
        })
    },
    loadMovieData: function ({ commit }) {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/loadmovielist/',
      })
        .then(res => {
          console.log(res)
          commit('GET_MOVIE_DATA', res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    loginLoadRecommendData: function ({ commit }) {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/loginrecommendmovielist/',
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` },
      })
        .then(res => {
          console.log(res)
          commit('GET_RECOMMEND_DATA', res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
    logoutLoadRecommendData: function ({ commit }) {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/logoutrecommendmovielist/'
      })
        .then(res => {
          console.log(res)
          commit('GET_RECOMMEND_DATA', res.data)
        })
        .catch(err => {
          console.log(err)
        })
      },
  },
  modules: {
  }
})
