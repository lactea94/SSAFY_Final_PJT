<template>
  <div>
    <div class="container d-block m-5 pb-5 mx-auto" style="color: white; background-color: rgba(0,0,0,0.5)">
      
      <h1 class="mb-auto p-5 text-center">{{ movieInfo.title }}</h1>

      <div class="row justify-content-center">
        <div class="col-4">
          <img :src="poster" alt="sample" class="card-image-sizing">
        </div>
        <div class="col-1">
        
        </div>
        <div class="col-5">
          <div class="d-flex align-items=start flex-column p-4" >
            <div class="p-2">
              {{ movieInfo.overview }}
            </div>
            <div class="p-2">
              개봉일 : {{ movieInfo.release_date }}
            </div>
            <div class="p-2">
              <vs-icon icon="star" v-for="index in movieInfo.user_rating" :key="index" size="15px" color="#ffd700"></vs-icon>
            </div>
            <div class= "p-2">
              <h4 v-show="isLike===true" class="fas fa-heart" @click="likeOrDislike"></h4>
              <h4 v-show="isLike===false" class="far fa-heart" @click="likeOrDislike"></h4>
            </div>
            <div class= "p-2">
              좋아요: {{ numLike }}
            </div>
            <div class="d-block mt-2">
              <h3> 리뷰 작성하기 </h3>
              <vs-textarea label="Review" v-model.trim="review_content" @keyup.enter="createReview" style="background-color: rgba(240,240,240,0.8 )"/>
              <vs-button type="gradient" @click="createReview">submit</vs-button>
              <vs-button type="gradient" @click="popupActivo4=true" class="mx-3">++ 리뷰 보기</vs-button>
            </div>
            <vs-popup fullscreen title="Current Reviews" :active.sync="popupActivo4">
              <div v-for="review in reviews" :key="review.id" class="container m-5 mx-auto p-5 rounded-2" style="color: white; background-color: rgba(0,0,0,0.5);">
                <div class="my-auto row">
                  <div class="col-md-2 mt-1" style="font-size: 1.2rem;">
                    <div><i class="fas fa-user-edit fa-fw"></i> {{ review.username }}</div>
                  </div>
                  <div class="col-md-5 mt-1" style="font-size: 1.2rem;">
                    <div><i class="fas fa-pen-nib fa-fw"></i> {{ review.content }}</div>
                  </div>
                  <div class="col-md-3 mt-1" style="font-size: 1.2rem;">
                    <div><i class="fas fa-list-alt fa-fw"></i> {{ review.created_at.slice(0,10)}} {{review.created_at.slice(11, 16)}} </div>
                  </div>
                  <div class="col-md-1">
                    <div>
                      <vs-button color="dark" type="gradient" @click="goReviewDetail(review)">자세히</vs-button>
                    </div>
                  </div>

                  <div class="col-md-1">
                    <span>
                      <vs-button color="dark" type="gradient" @click="deleteReview(review)">delete</vs-button>
                    </span>
                  </div>
                </div>
              </div>
            </vs-popup>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
  name: 'Detail',
  data: function () {
    return {
      movieId: '',
      movieInfo: [],
      poster: '',
      reviews: '',
      review_content: '',
      review_content_modi: '',
      numLike: '',
      isLike: false,
      popupActivo4: false,
    }
  },
  methods: {
    createReview: function () {
      const content = this.review_content
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/review_create/${this.movieId}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` },
        data: {
          content,
        }
      })
        .then(res => {
          this.reviews.unshift(res.data)
          this.review_content = ''
          Swal.fire({
            title: '리뷰가 등록되었습니다!',
            timer: 1000,
            timerProgressBar: true,
          })
        })
        .catch(err => {
          console.log(err)
        })
    },
    deleteReview: function (review) {
      const reviewPk = review.review_pk
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/movies/review_update_delete/${this.movieId}/${reviewPk}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` }
      })
       .then(() => {
        axios({
          method: 'get',
          url: `http://127.0.0.1:8000/movies/review_list/${this.$route.params.moviePk}/`
        })
          .then(res => {
            console.log(res)
            this.reviews = res.data
          })
       })
       .catch(err => {
         console.log(err)
       })
    },
    likeOrDislike: function () {
      axios({
          method: 'post',
          url: `http://127.0.0.1:8000/movies/movie_like/${this.movieId}/`,
          headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` }
        })
          .then(res => {
            console.log(res.data)
            if (res.data.data === "like") {
              this.isLike = true
              this.numLike += 1
            } else {
              this.isLike = false
              this.numLike -= 1
            }
          })
          .catch(err => {
            console.log(err)
          })
    },

    goReviewDetail: function (review) {
      this.$router.push({ name: 'ReviewDetail', params: { reviewPk: review.review_pk, data: review } })
    },
  },
  created: function () {
    console.log(this.$route.params.moviePk)
    this.movieId = this.$route.params.moviePk
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/movies/detail/${this.$route.params.moviePk}/`
    })
      .then(res => {
        this.movieInfo = res.data
        this.poster = `https://image.tmdb.org/t/p/original${res.data.poster_path}`
      })
      .catch(err => {
        console.log(err)
      })
    
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/movies/review_list/${this.$route.params.moviePk}/`
    })
      .then(res => {
        this.reviews = res.data
      })
      .catch(err => {
        console.log(err)
      })
    if (localStorage.getItem('jwt')) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/login_get_movie_like/${this.movieId}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` }
      })
        .then(res => {
          console.log(res.data)
          this.numLike = res.data.likenumber
          if (res.data.data === "like") {
            this.isLike = true
          } else if (res.data.data === "dislike") {
            this.isLike = false
          }
        })
        .catch(err => {
          console.log(err)
        })
    } else {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/logout_get_movie_like/${this.movieId}/`,
      })
        .then(res => {
          console.log(res.data)
          this.numLike = res.data.likenumber
          if (res.data.data === "like") {
            this.isLike = true
          } else if (res.data.data === "dislike") {
            this.isLike = false
          }
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style>
.card {
  flex-direction: row;
}
.flex-container{
  display: flex;
  margin: 5em;
}

.textarea {
  width: 506px;
  height: 150px;
}

.card-image-sizing{
  max-width: 100%;
  height: auto;
}
.moviecontent {
  color: white;
  font-family: 'Gotham Black 500', sans-serif;
  font-size: 1.5rem;
}

</style>
