<template>
  <div class="open-page">
    <div class="open"></div>
    <div class="card openingbox">
      <div class="card-body">
        <p class="card-text content">단지 두려움 때문에</p>
        <p class="card-text content">좋아하는 일을 포기하지 마</p>
        <p class="card-text content">- Sing, 2016 -</p>
        <div class="logos">
          <i class="fas fa-home fa-2x fa-fw" @click="goMovie"></i>
          <i class="fas fa-plus fa-2x fa-fw" @click="goLogin"></i>
          <i class="fas fa-sign-in-alt fa-2x fa-fw" @click="goSignup"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Main',

  methods: {
    goMovie: function () {
      this.$router.push({ name: 'Movie'})
    },
    goLogin: function () {
      this.$router.push({ name: 'Login'})
    },
    goSignup: function () {
      this.$router.push({ name: 'Signup'})
    }
  }
}
</script>

<style>

.open-page {
  position: fixed;
  top: 0; 
  left: 0; 
  margin: auto;
  width: 100vw;
  height: 100vh;
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("https://variety.com/wp-content/uploads/2021/10/sing-2.jpg");
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
}
.open {
  display: flex;
  justify-content: center;
  align-items: center;
}
@import url('http://fonts.cdnfonts.com/css/gotham?styles=17581,17589,17591');

.card-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  
}
.content {
  font-family: 'Gotham Black 500', sans-serif !important;
  font-size: 1rem !important;
  padding: 2px;
}
.openingbox {

  width: 300px;
  height: 400px;
  background-color: rgba(0, 0, 0, 0.6);
  text-align: center;
  color: white
}
.logos {
  z-index: 6;
  display: flex;
  justify-content: space-evenly;
  padding: 20px;
}
</style>