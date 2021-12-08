<template>
  <div class="col">
    <div style="max-width: 100%; height: auto;">
      <div>
        <div @click="popupActivo4=true" @mouseover="isOver=true" @mouseleave="isOver=false" class="card bg-dark text-white" :class="info">
          <carousel-list :movies="movies" :isOver="isOver" style="max-width: 100%; height: auto;" >
          </carousel-list>
          <div class="card-img-overlay text-center" v-show="isOver">
            <h5 class="card-title gothamblack"><i class="fas fa-user-edit fa-fw"></i>{{ index }}</h5>
            <p class="card-text gotham"><i class="fas fa-list-alt fa-fw"></i>{{ playList[1] }}</p>
          </div>
        </div>
      </div>
      <vs-popup fullscreen :title="index" :active.sync="popupActivo4">
        <div class="container">
          <div class="row">
            <div class="col">
              <div style="font-size: 50px;">
                <i class="fas fa-pen-nib fa-fw"></i>
                {{ playList[0] }}
              </div>
            </div>
            <hr>
            <div class="col">
              <div style="font-size: 30px;">
                <i class="fas fa-user-edit fa-fw"></i>
                {{ index }}
              </div>
              <div style="font-size: 30px;">
                <i class="fas fa-list-alt fa-fw"></i>
                {{ playList[1]}}
              </div>
            </div>
            <hr>
          </div>
        </div>
        <div>
          <vs-row vs-justify="space-around">
            <vs-col class="mx-2" type="flex" vs-justify="center" vs-align="center" vs-lg="3" vs-sm="6" vs-xs="12" v-for="(movie, index1) in movies" :key="index1">
              <vs-card actionable class="cardx" fixedHeight>
                <div slot="header">
                  <h4>{{ movie.title }}</h4>
                </div>
                <div slot="media">
                  <img :src="getPoster(movie)" alt="sample" @click="goDetail(movie)">
                </div>
                <div>
                  {{ cutOverview(movie.overview) }}
                </div>
                <div slot="footer" style="width: 250px;">
                  <vs-row vs-type="flex" vs-justify="flex-end">
                    <vs-icon icon="star" v-for="index in movie.user_rating" :key="index" size="15px" color="#ffd700"></vs-icon>
                  </vs-row>
                  <vs-row vs-type="flex" vs-justify="flex-end">
                    <div>{{ getGenre(movie.genre_code) }} / {{ convertDate(movie.release_date) }}</div>
                  </vs-row>
                </div>
              </vs-card>
            </vs-col>
          </vs-row>
        </div>
      </vs-popup>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import CarouselList from '@/components/CarouselList.vue'

export default {
  name: 'PlayListItem',

  components: {
    CarouselList
  },

  data: function () {
    return {
      popupActivo4: false,
      movies: [],
      isOver: false,
    }
  },

  props: {
    playList: Array,
    index: String,
  },

  methods: {
    getMovies: function (movieids) {
      const ids = movieids.join('-')
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/userplaylist/movies/${ids}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` },
      })
        .then(res => {
          this.movies = res.data
        })
        .catch(err => {
          console.log(err)
        })
      this.popupActivo4=true
    },
    getPoster: function (movie) {
      const poster_path = `https://image.tmdb.org/t/p/original${movie.poster_path}`
      return poster_path
    },
    getGenre: function (gen) {
      let genres = gen.replace('[', '')
      genres = genres.replace(']', '')
      return genres
    },
    cutOverview: function (overview) {
      let shorten = ''
      if (overview.length >= 150) {
        shorten = overview.slice(0, 151) + '...'
        return shorten
      } else {
        return overview
      }
    },
    convertDate: function (time) {
      const tmp = time.split('-')
      const result = tmp.slice(0, 2).join('.')
      return result
    },
    goDetail: function (movie) {
      this.$router.push({ name:'Detail', params: { moviePk: movie.auto_increment_id } } )
    },

  },
  created: function () {
    const ids = this.playList[2].join('-')
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/userplaylist/movies/${ids}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` },
      })
        .then(res => {
          this.movies = res.data
        })
        .catch(err => {
          console.log(err)
        })
    
  },
  computed: {
    info: function () {
      if (this.isOver) {
        return { infomation: true }
      } else {
        return { infomation: false}
      }
    },
  }
}
</script>

<style>
@import url('http://fonts.cdnfonts.com/css/gotham?styles=17581,17589,17591');

.infomation {
  filter: opacity(0.9) drop-shadow(0, 0, 0);
}

.gothamblack {
  font-family: 'Gotham Black 500', sans-serif;
  font-size: 2.3rem;
}
.gotham {
  font-family: 'Gotham 500', sans-serif;
  font-size: 1.5rem;
}
.brightness {
  -webkit-filter: brightness(0.30);
  filter: brightness(0.30);
}

</style>