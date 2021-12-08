<template>
  <div>
    <div id="app" class="container">
      <!-- 배경 -->

      <div class="back-container">
        <img class="background" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/221808/sky.jpg"/>
      </div>

      <div class="row">
        <div id="parentx" class="container">
          <i class="sidebar-btn fas fa-arrow-circle-right fa-2x fixed-top p-4" @click="changeActive" style="color:white"></i>
          <vs-sidebar parent="body" default-index="1" color="primary" class="sidebarx" spacer v-model="active">
            <div class="header-sidebar ms-2 row" slot="header">
              <i class="fas fa-user fa-2x col-2"></i>
              <h4 class="col-1">{{ myUsername }}</h4>
            </div>
            <vs-sidebar-item index="1" class="row ms-1" :to="{ name: 'Movie'}" style="max-width: 95%;" @click="changeActive">
              <i class="fas fa-home fa-2x fa-fw col-1"></i>
              <div class="fs-6 col-1 offset-1" >
                Movie
              </div> 
            </vs-sidebar-item>
            <div v-if="isLogin">
              <vs-sidebar-item index="2" class="row ms-1" :to="{ name: 'Playlist' }" style="max-width: 95%;" @click="changeActive">
                <i class="fas fa-clipboard-list fa-2x fa-fw col-1"></i>
                <div class="fs-6 col-1 offset-1">
                  PlayList
                </div> 
              </vs-sidebar-item>
              <vs-divider icon="person" position="left">
              </vs-divider>
              <vs-sidebar-item index="3" class="row ms-1" :to="{ name: 'Profile', params: { username: myUsername }}" style="max-width: 95%;" @click="changeActive">
                <i class="fas fa-id-badge fa-2x fa-fw col-1"></i>
                <div class="fs-6 col-1 offset-1">
                  Profile
                </div> 
              </vs-sidebar-item>
              <vs-sidebar-item index="4" class="row ms-1" @click.native="logout()" to="#" @click="changeActive" style="max-width: 95%;">
                <i class="fas fa-sign-out-alt fa-2x fa-fw col-1"></i>
                <div class="fs-6 col-1 offset-1">
                  logout
                </div>
              </vs-sidebar-item>
            </div>
            <div v-else>
              <vs-sidebar-item index="2" class="row ms-1" :to="{ name: 'Signup' }" style="max-width: 95%;" @click="changeActive">
                <i class="fas fa-plus fa-2x fa-fw col-1"></i>
                <div class="fs-6 col-1 offset-1" >
                  Signup
                </div>
              </vs-sidebar-item>
              <vs-sidebar-item index="3" class="row ms-1" :to="{ name: 'Login' }" style="max-width: 95%;" @click="changeActive">
                <i class="fas fa-sign-in-alt fa-2x fa-fw col-1"></i>
                <div class="fs-6 col-1 offset-1" >
                  Login
                </div>
              </vs-sidebar-item>
            </div>
          </vs-sidebar>
        </div>
      </div>
      <router-view/>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex"

export default {
  name: 'App',

  data: function () {
    return {
      active: false
    }
  },

  methods: {
    ...mapActions([
      'logout',
    ]),
    changeActive: function () {
      this.active = !this.active
      // console.log(this.active)
    },

 
  },
  computed: {
    ...mapGetters([
      'isLogin'
    ]),
    ...mapState([
      'myUsername'
    ])
  },
  created: function () {
    this.$store.dispatch('loadMovieData')
  },
}
</script>


<style>

@import url('http://fonts.cdnfonts.com/css/gotham?styles=17581,17589,17591');

.gotham{
  font-family: 'Gotham Black 500', sans-serif;
  font-size: 5rem;
}

.image-size {
  width: 150px;
  height: 100px;
  position: absolute;
  top: 10px;
  left: 221px;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  margin: 0;
  min-height: 100vh;
  min-width: 100vw;
  z-index: 0;
  /* background: #102a43; */
  /* background-image: url("https://s3-us-west-2.amazonaws.com/s.cdpn.io/221808/sky.jpg"); */
  background-size: contain;
}

.sidebar-btn {
  max-width: 5%;
  height: auto;
}

.background {
  display: block;
  z-index: -2;
  position: absolute;
  top: 0;
  left: 0;
  object-fit: cover;
  width: 100%;
  height: 100%;
  /* mask-image: radial-gradient(
    rgb(0, 0, 0) 0%,
    rgb(0, 0, 0) 60%,
    transparent 90%,
    transparent
  ); */
}

/* .message {
  position: absolute;
  right: 20px;
  bottom: 10px;
  color: white;
  font-family: "Gotham Black 500", serif;
  line-height: 27px;
  font-size: 18px;
  text-align: right;
  pointer-events: none;
  animation: message-frames 1.5s ease 5s forwards;
  opacity: 0;

}
@keyframes message-frames {
    from {
      opacity: 0;
    }
    
    to {
      opacity: 1;
    }
} */


</style>
