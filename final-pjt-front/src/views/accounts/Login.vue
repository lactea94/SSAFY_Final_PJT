<template>
  <div class="container container-style" style="background-color: rgba(0, 0, 0, 0.5)">
    <div class="row g-3">
      <div class="col-11 mx-auto">
        <label for="username" class="form-label" style="color: white; font-family: gotham">username</label>
        <input type="text" class="form-control" id="username" v-model="credentials.username">
      </div>
      <div class="col-11 mx-auto">
        <label for="password" class="form-label" style="color: white; font-family: gotham">Password</label>
        <input type="password" class="form-control" id="password" v-model="credentials.password">
      </div>
      <div class="col-2">
        <vs-button type="gradient" style="font-size: 2.5rem; margin: 2.4rem; width: 120px;" @click="isValid(credentials)" @keyup.enter="isValid(credentials)">log in</vs-button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex"
import Swal from 'sweetalert2'

export default {
  name: 'Login',
  data: function () {
    return {
      credentials: {
        username: '',
        password: '',
      }
    }
  },
  methods: {
    ...mapActions([
      'login',
    ]),
    isValid: function (cred) {
      if (cred.username === '' || cred.password === '') {
        Swal.fire({
          icon: 'error',
          title: 'Stop!',
          text: '모두 필수 입력사항입니다.',
        })
      } else {
        this.login(cred)
      }
    },
  },
}
</script>

<style>
.container-style {
  width: 1000px;

  margin-top: 15rem;
  font-size: 4rem;
}

.box-size {
  margin-top: 1rem;
  width: 9rem;
  height: 3rem;
}
</style>