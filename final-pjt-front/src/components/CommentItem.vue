<template>
  <div class="ibox-content forum-container m-4" style="color: white;">
    <div class="commentlist">
      <div class="contentbox">
        <div><i class="fas fa-user-edit fa-fw"></i>작성자 {{ comment.username }}</div>
        <div><i class="fas fa-pen-nib fa-fw"></i> {{ comment.content }}</div>
        <div><i class="fas fa-list-alt fa-fw"></i> {{ comment.created_at.slice(0,10)}} {{comment.created_at.slice(11, 16)}} </div>
        <vs-input type="text" @keyup.enter="updateComment(comment)" v-model.trim="commentContentModi" class="mb-2" style="color: black"/>
        <vs-button color="dark" type="gradient" @click="updateComment(comment)">댓글 수정</vs-button>
        <vs-button color="dark" type="gradient" @click="deleteComment(comment)">Delete</vs-button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CommentItem',
  data: function () {
    return {
      commentContentModi: '',
    }
  },
  props: {
    comment: Object,
  },
  methods: {
    updateComment: function (comment) {
      console.log(comment)
      const commentItem = {
        ...comment,
        content: this.commentContentModi,
      }
      console.log(commentItem)
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/movies/commentupdate_or_delete/${comment.review}/${comment.comment_pk}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` },
        data: {
          commentItem
        }
      })
        .then(res => {
          console.log(res)
          console.log(this.comment)
          this.comment.content = res.data.content
        })
        .catch(err => {
          console.log(err)
        })
    },
    deleteComment: function (comment) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/movies/commentupdate_or_delete/${comment.review}/${comment.comment_pk}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` },
      })
        .then(res => {
          console.log(res)
          this.$emit('comment-delete-change', res.data)
        })
        .catch(err => {
          console.log(err)
          console.log(comment)
        })
    }
  }
}
</script>

<style>

@import url('http://fonts.cdnfonts.com/css/gotham?styles=17581,17589,17591');

.contentbox {
  display: flex;
  justify-content: space-evenly;
}
.contentbox > div {
  font-size: 1.2rem;
  font-family: 'Gotham 500', sans-serif !important;
  margin-top: 2px
}
</style>