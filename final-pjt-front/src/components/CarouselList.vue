<template>
  <hooper :progress="true" :autoPlay="true" :playSpeed="5000">
    <slide v-for="(movie, index) in movies" :key="index">
      <img :src="getPoster(movie)" alt="sample" :class="info">
    </slide>
  </hooper>
</template>

<script>
  import { Hooper, Slide } from 'hooper'
  import 'hooper/dist/hooper.css'

  export default {
    name: 'CarouselList',
    components: { 
      Hooper,
      Slide
    },
    props: {
      movies: Object,
      isOver: Boolean
    },
    data: function () {
      return {
        
      }
    },
    methods: {
      getPoster: function (movie) {
      const poster_path = `https://image.tmdb.org/t/p/original${movie.poster_path}`
      return poster_path
      },
    },
    computed: {
      info: function () {
        if (this.isOver) {
          return { brightness: true }
        } else {
          return { brightness: false}
        }
      },
    }
  }
</script>

<style>
.brightness {
  -webkit-filter: brightness(0.30);
  filter: brightness(0.30);
}
img {
  max-width: 100%; 
  height: auto;
}
</style>