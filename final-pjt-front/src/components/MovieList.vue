<template>
  <div>
    <div class="card bg-dark text-white" @click=goDetail() @mouseover="isOver=true" @mouseleave="isOver=false">
      <img :src="getPoster(movie)" alt="sample" :class="info">
      <div class="card-img-overlay text-center" v-show="isOver">
        <h5 class="card-title my-4">{{ movie.title }}</h5>
        <p class="card-text">{{ cutOverview() }}</p>
      </div>
    </div>
  </div>
</template>
<script>

export default {
  name: 'MovieList',
  data: function () {
    return {
      poster_path: '',
      short_overview: '',
      isOver: false,
    }
  },
  props: {
    movie: Object
  },
  methods: {
    getPoster: function () {
      this.poster_path = `https://image.tmdb.org/t/p/original${this.movie.poster_path}`
      return this.poster_path
    },
    cutOverview: function () {
      const shorten = this.movie.overview.slice(0, 101) + '...'
      this.short_overview = shorten
      return this.short_overview
    },
    goDetail: function () {
      this.$router.push({name:'Detail', params: {moviePk: this.movie.auto_increment_id}})
    },
  },
  watch: {
    isOver: function (newVal, oldVal) {
      if (newVal === true & oldVal === false) {
        this.$emit('movie-poster-pass', this.poster_path)
      } else if (newVal === false & oldVal === true) {
        this.$emit('movie-poster-return')
      }
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
.card-title {
  font-family: 'Gotham Black 500', sans-serif;
  font-size: 1.3rem;
}
.card-text {
  font-family: 'Gotham 400', sans-serif;
  font-size: 0.8rem;
}
</style>