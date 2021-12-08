<template>
  <div class="movie-page">
    <div class="movie"></div>
      <div class="title">Movies</div>
      <div class="carousel">
        <hooper class="hooper" :itemsToShow="8" :progress="true">
          <slide v-for="(movie, index1) in movies" :key="index1" class="slide mx-3">
            <movie-list :movie="movie" class="movielist" >
            </movie-list>
          </slide>
        </hooper>
      </div>

      <h1 class="title">Recommends</h1>
      <div class="carousel">
        <hooper class="hooper" :itemsToShow="8" :progress="true">
          <slide v-for="(recommend, index2) in recommends" :key="index2" class="slide mx-3">
            <recommend-list  :recommend="recommend" class="recommendlist">
            </recommend-list>
          </slide>
        </hooper>
      </div>
  </div>
</template>


<script>
import { mapGetters, mapState } from 'vuex'
import { 
  Hooper, 
  Slide, 
  } from 'hooper'
import MovieList from '@/components/MovieList.vue'
import RecommendList from '@/components/RecommendList.vue'
import 'hooper/dist/hooper.css'

export default {
  name: 'Movie',
  components: {
    MovieList,
    RecommendList,
    Hooper,
    Slide,
  },
  data: function () {
    return {
      Path: "",
    }
  },
  methods: {
    getPosterPath: function (inputData) {
      this.Path = inputData
    },
    deletePosterPath: function () {
      this.Path = ''
    },
    
  },

 
  computed: {
    ...mapState(['movies', 'recommends']),
    ...mapGetters(['isLogin']),
    
  },
  created: function () {
    if (this.isLogin) {
      this.$store.dispatch('loginLoadRecommendData')
    } else {
      this.$store.dispatch('logoutLoadRecommendData')
    }
  },
}
</script>

<style>
@import url('http://fonts.cdnfonts.com/css/gotham?styles=17581,17589,17591');

#bg {
  position: fixed;
  z-index: -1;
  top: 0;
  left: 0;
  margin: auto;
}

.movie-page {
  position: fixed;
  z-index: 3;
  width: 100vw;
  height: 100vh;
}
.title {
  font-family: 'Gotham Black 500', sans-serif;
  font-size: 3rem;
  color: white;
  margin: 15px 70px;
}
.movie {
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel {
  align-self: center;
}

.hooper {
  max-width: 100%;
  height: auto;
}

.movielist {
  max-height: 80%;
  width: auto;
}

.recommendlist {
  max-height: 80%;
  width: auto;
}

.page {
  max-width: 5%;
  height: auto;
}
.gothamblack {
  font-family: 'Gotham Black 500', sans-serif;
  font-size: 1.5rem;
}
.page {
  max-width: 5%;
  height: auto;
}
</style>