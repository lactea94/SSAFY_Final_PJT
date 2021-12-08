<template>
  <div>
    <div class="container">
      <div>
        <div class="Playliststyle text-center">All User's Playlists</div>
      </div>
      <div class="row row-cols-3">
        <play-list-item v-for="(playList, index) in playLists" :key="index" :playList="playList" :index="index">
        </play-list-item>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import PlayListItem from '@/components/PlayListItem.vue'

export default {
  name: 'Playlist',
  data: function () {
    return {
      playLists: [],
    }
  },

  components: {
    PlayListItem,
  },

  methods: {
  },
  created: function () {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/movies/userplaylist/`,
      headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` }
    })
      .then(res => {
        console.log(res)
        this.playLists = res.data
      })
      .catch(err => {
        console.log(err)
      })
  },
}
</script>

<style>

.Playliststyle {
  
  font-size : 5rem;
  color: white;
  margin: 3rem;
  font-family: "gotham Black", sans-serif;
}
</style>