<template>
  <div>
    <div class="container mx-auto profilebox" style="color: white; background-color: rgba(0, 0, 0, 0.5)">
      <div class="row">
        <h1 class="text-center mt-4 buttontext">{{ username }}'s Profile</h1>
        <div>
          <div class="m-4 text-center" >
            {{ myText }}
          </div>

          <div class="m-4 text-center">
            <div v-if="myText === ''">
              <input type="text" placeholder="자기소개를 써주세요" @keyup.enter="createInterest" v-model.trim="content">
            </div>
            <div v-else>
              <input type="text" placeholder="자기소개 변경하기" @keyup.enter="createInterest" v-model.trim="content">
            </div>
          </div>

          <div class="m-2 text-center">
            <div>좋아요한 장르 개수 : {{likeGenre.length-1}}</div>
            <div v-if="likeGenre.length===1">선호하는 장르가 아직 없습니다</div>
            <div v-else> {{customGenre}}</div>
          </div>
          <hr>

        </div>
        <div class="text-center p-4"><h1> 영화 추천을 받을 장르를 선택하세요 </h1></div>
        <div class="text-center">
          <div>
            <input type="checkbox" id="action" value="액션" v-model="likeGenre"><label for="action">액션</label>
            <input type="checkbox" id="adventure" value="모험" v-model="likeGenre"><label for="adventure">어드벤쳐</label>
            <input type="checkbox" id="animation" value="애니메이션" v-model="likeGenre"><label for="animation">애니메이션</label>
            <input type="checkbox" id="comedy" value="코미디" v-model="likeGenre"><label for="comedy">코미디</label>        
            <input type="checkbox" id="crime firm" value="범죄" v-model="likeGenre"><label for="crime firm">범죄</label>
            <input type="checkbox" id="documentary" value="다큐멘터리" v-model="likeGenre"><label for="documentary">다큐멘터리</label>
            <input type="checkbox" id="drama" value="드라마" v-model="likeGenre"><label for="drama">드라마</label>
          </div>
          <div>
            <input type="checkbox" id="family" value="가족" v-model="likeGenre"><label for="family">가족</label>
            <input type="checkbox" id="fantasy" value="판타지" v-model="likeGenre"><label for="fantasy">판타지</label>
            <input type="checkbox" id="history" value="역사" v-model="likeGenre"><label for="history">역사</label>
            <input type="checkbox" id="horror" value="호러" v-model="likeGenre"><label for="horror">호러</label>
            <input type="checkbox" id="music" value="음악" v-model="likeGenre"><label for="music">음악</label>
            <input type="checkbox" id="mystery" value="미스터리" v-model="likeGenre"><label for="mystery">미스터리</label>
            <input type="checkbox" id="romance" value="로맨스" v-model="likeGenre"><label for="romance">로맨스</label>
          </div>
          <div>
            <input type="checkbox" id="SF" value="SF" v-model="likeGenre"><label for="SF">SF</label>
            <input type="checkbox" id="TV movie" value="TV 영화" v-model="likeGenre"><label for="TV movie">TV 영화</label>
            <input type="checkbox" id="thriller" value="스릴러" v-model="likeGenre"><label for="thriller">스릴러</label>
            <input type="checkbox" id="military" value="전쟁" v-model="likeGenre"><label for="military">전쟁</label>
            <input type="checkbox" id="western" value="서부" v-model="likeGenre"><label for="western">서부</label>
          </div>
          <div>
          </div>
          <vs-button color="dark" type="gradient" @click="createInterest" class="m-4 minibutton"> <div class="textnum2"> 선호장르 변경하기 </div> </vs-button>
        </div>
      </div>
    </div>

    <br>
    <hr>
    <br>
    <div class="container">
      <div class="row">
        <vs-button type="gradient" @click="popupActivo4=true" class="gotham buttonsize" >
          <p class="buttontext"> Create your Own Playlist! </p>
        </vs-button>
      </div>
    </div>
    <vs-popup fullscreen title="fullscreen" :active.sync="popupActivo4">
      <div class="container bg-white">
        <div class="m-2 p-3 row" >
          <div class="form-group text-center m-4">
            <label for="title" class="innertext">플레이리스트 제목(필수)</label>
            <vs-textarea type="text" class="form-control" id="title" v-model="introPlaylist.title"></vs-textarea>
          </div>
          <div class="form-group text-center text m-4">
            <label for="content" class="innertext">내용(필수)</label>
            <vs-textarea class="form-control" id="content" rows="3" v-model="introPlaylist.content"></vs-textarea>
          </div>
        </div>
        <div class="container">
          <div class="mb-3 px-5 row fs-3">  

            <div v-if="introPlaylist.movielist.length===0" class="text-center mx-auto"> 등록하려면 영화를 검색 후 추가하세요 </div>
            <div v-else-if ="introPlaylist.movielist.length===1" class="text-center mx-auto">{{ introPlaylist.movielist[0] }}</div>
            <div v-else class="text-center mx-auto"> 선택된 영화 : {{ introPlaylist.movielist.join(', ') }}</div> 

            <vs-button color="dark" type="gradient" class="mx-auto createtext mt-4" @click="createUserPlaylist">Playlist Create</vs-button>
            <div class="mx-3 text-center mx-auto mt-4 mb-5">
              <label for="search" class="mx-3">search for</label>
              <input type="text" id="search" @keyup.enter="submitSearch" v-model="searchData">
            </div>  
          </div>
        </div>
      </div>

      <div class="container">
        <div class="row">
          <div v-for="(searchedDatum, index) in searchedData" :key="index" class="col-4 mb-5">
            <img class="card-img-top" :src="getPoster(searchedDatum.poster_path)" alt="Card image cap" :for="searchedDatum.title">
            <input type="checkbox" :id="searchedDatum.title" :value="searchedDatum.title" v-model="introPlaylist.movielist">
          </div>
        </div>
      </div>
    </vs-popup>




  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'


export default {
  name: 'Profile',

  data: function () {
    return {
      innertext: "소개글 변경하기",
      popupActivo4:false,
      username: '',
      likeGenre: '',
      customGenre: '',
      content: '',
      myText: '',
      myGenres: '',
      introPlaylist: {
        username: null,
        title: null,
        content: null,
        movielist: [],
      },
      searchData: '',
      searchedData: [],
    }
  },

  methods: {
    createInterest: function () {
      const likeGenre = this.likeGenre
      const content = this.content
      axios({
        method: 'put',
        url: 'http://127.0.0.1:8000/accounts/profile/update/',
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` },
        data: {
          likeGenre,
          content,
        }
      })
        .then(res => {
          console.log(res)
          this.myText = content
          this.customGenre = likeGenre.join(", ").slice(1)
        })
        .catch(err => {
          console.log(err)
        })
    },
    createUserPlaylist: function () {
      const introduce = {
        ...this.introPlaylist,
        username: this.username,
      }
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/movies/userplaylist/add/',
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` },
        data: {
          introduce
        },
      })
        .then(res => {
          console.log(res)
          this.$router.push({ name: 'Playlist' })
        })
        .catch(err => {
          console.log(err)
        })
    },
    submitSearch: function () {
      const search = this.searchData
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/search/${search}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` },
        data: {
          search
        }
      })
        .then(res => {
          console.log(res)
          this.searchedData = res.data
          this.searchData = ''
        })
        .catch(err => {
          console.log(err)
        })
    },
    getPoster: function (poster_path) {
      const poster = `https://image.tmdb.org/t/p/original${poster_path}`
      return poster
    },
  },

  created: function () {
    this.username = this.$route.params.username
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/profile/${this.username}/`,
      headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` }
    })
      .then(res => {
        console.log(res)
        this.myText = res.data.content
        const tmpGenre = res.data.genre.split('/')
        console.log(tmpGenre)
        this.likeGenre = tmpGenre
        this.customGenre = this.likeGenre.join(", ").slice(1)
      })
      .catch(err => {
        console.log(err)
      })
  },

  computed: {
    ...mapState([ 'movies' ]),
  },
}
</script>

<style>
.profilebox {
  z-index: 1;
  margin-top: 14rem;
}
.createtext {
  font-size: 5rem;
  width: 700px;
  height: 150px;
}
 
.buttonsize {
  margin: auto;
  width: 700px;
  height: 130px;
  text-decoration-color: black;
}

.innertext{
  font-family: 'Gotham Black 500', sans-serif;
  font-size: 3rem;
}

.buttontext{
  font-family: 'Gotham Black', sans-serif;
  font-size: 3rem;
}

.minibutton {
  width: 200px;
  height: 50px;
  color: white;
  background-color: black;

}

.textnum2 {
  font-size: 1.2rem;
  font-family: 'Gotham Black', sans-serif;
}

</style>