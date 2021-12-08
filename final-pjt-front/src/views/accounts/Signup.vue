<template>
  <div class="container container-style" style="background-color: rgba(0, 0, 0, 0.5)">
    <div class="row g-3 ">
      <div class="col-11 mx-auto">
        <label for="username" class="form-label" style="color: white; font-family: gotham">username</label>
        <input type="text" class="form-control box-size" id="username" v-model="credentials.username">
      </div>
      <div class="col-11 mx-auto">
        <label for="password" class="form-label" style="color: white; font-family: gotham">Password</label>
        <input type="password" class="form-control box-size" id="password" v-model="credentials.password">
      </div>  
      <div class="col-11 mx-auto">
        <label for="passwordConfirmation" class="form-label" style="color: white; font-family: gotham">passwordConfirmation</label>
        <input type="password" class="form-control box-size" id="passwordConfirmation" v-model="credentials.passwordConfirmation">
      </div>
      <div class="col-2">
        <vs-button type="gradient" style="font-size: 3rem; margin: 2.4rem"  @click="isValid(credentials)">SignUp</vs-button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import Swal from 'sweetalert2'

export default {
  name: 'Signup',
  data: function () {
    return {
      credentials: {
        username: '',
        password: '',
        passwordConfirmation: '',
      },
      popupActivo4: true,
    }
  },

  methods: {
    ...mapActions([
      'signup'
    ]),
    isValid: function (cred) {
      if (cred.username === '' || cred.password === '' || cred.passwordConfirmation === '') {
        Swal.fire({
          icon: 'error',
          title: 'Stop!',
          text: '모두 필수 입력사항입니다.',
        })
      } else if (cred.password !== cred.passwordConfirmation) {
        Swal.fire({
          icon: 'error',
          title: 'Oops..',
          text: '잘못된 입력입니다.',
        })
      } else {
        this.signup(cred)
      }
    }
  }
}
</script>

<style>
.container-style {
  margin-top: 15rem;
  font-size: 4rem;
}

.box-size {
  margin-top: 1rem;
  width: 5rem;
  height: 3rem;
}
</style>