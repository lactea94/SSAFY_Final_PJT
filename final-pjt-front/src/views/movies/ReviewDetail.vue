<template>
  <div>
    <div class="container" style="color: white; margin-top: 50px">
      <div class="row">
        <div class="ibox-content forum-container m-4">
          <h1 class="d-block p-2 text-center">{{ reviewData.username }}의 리뷰</h1>
        </div>
        <div class="ibox-content forum-container m-4">
          <div class="reviewbox">
            <h3 style=""><i class="fas fa-pen-nib fa-fw"></i></h3>
            <div class="card-text" style="font-size: 1.3rem;">{{ this.reviewData.content }}</div>
            <vs-button color="dark" type="gradient" @click="popupActivo2=true" style="width: 100px; align-self: flex-end">리뷰 수정</vs-button>
            <div>
              <vs-popup title="Modify Review" :active.sync="popupActivo2">
                <div class="m-5">
                  <h2 class="text-center">리뷰 수정하기</h2>
                  <vs-textarea label="modifiy review" @keyup.enter="updateReview" v-model="reviewContentModi" class="reviewmodified-sizing" style="background-color: rgba(240,240,240,0.8 )"/>
                  <br>
                  <vs-button color="dark" type="gradient" @click="updateReview">내 리뷰 수정하기</vs-button> 
                </div>
              </vs-popup>
              <div class="m-5">
                <h3 class="text-center"> 코멘트 작성 </h3>
                <vs-textarea label="Comment" @keyup.enter="createComment" v-model="commentContent" class="commentcreate-sizing" style="background-color: rgba(240,240,240,0.8 )"/>
                <div class="buttons">
                  <vs-button color="dark" type="gradient" @click="createComment">submit</vs-button>
                  <vs-button color="dark" type="gradient" @click="popupActive=true">보기</vs-button>
                </div>
              </div>
              <vs-popup fullscreen title="Comments"  :active.sync="popupActive">
                <div class="container">
                  <div class="row">
                    <comment-item v-for="comment in comments" :key="comment.id" :comment="comment" @comment-delete-change="commentChange">
                    </comment-item>
                  </div>
                </div>
              </vs-popup>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import CommentItem from '@/components/CommentItem.vue'
import Swal from 'sweetalert2'

export default {
  name: 'ReviewDetail',
  components: {
    CommentItem,
  },
  data: function () {
    return {
      reviewId: '',
      reviewData: '',
      reviewContentModi: '',
      commentContent: '',
      comments: [],
      popupActivo2: false,
      popupActive: false,
    }      
  },
  methods: {
    updateReview: function () {
      const reviewItem = {
        ...this.reviewData,
        content: this.reviewContentModi,
      }
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/movies/review_update_delete/${this.reviewData.movie}/${this.reviewData.review_pk}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` },
        data: {
          reviewItem,
        }
      })
        .then(res => {
          console.log(res)
          this.reviewData.content = this.reviewContentModi
          this.popupActivo2 = false
        })
        .catch(err => {
          console.log(err)
          Swal.fire({
            icon: 'error',
            title: 'Stop!',
            text: '작성자가 아닙니다!.',
          })
        })
    },
    createComment: function () {
      const content = this.commentContent
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/commentlist_or_create/${this.reviewId}/`,
        headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` },
        data: {
          content
        }
      })
        .then(() => {
          axios({
            method: 'get',
            url: `http://127.0.0.1:8000/movies/commentlist_or_create/${this.reviewId}/`,
            headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` }
          })
            .then(res => {
              console.log(res)
              this.comments = res.data
            })
            .catch(err => {
              console.log(err)
            })
        })
        .catch(err => {
          console.log(err)
        })
    },
    commentChange: function (input) {
      this.comments = input
    }
  },
  created: function () {
    this.reviewId = this.$route.params.reviewPk


    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/movies/commentlist_or_create/${this.reviewId}/`,
      headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` }
    })
      .then(res => {
        console.log(res)
        this.comments = res.data
      })
      .catch(err => {
        console.log(err)
      })
      
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/movies/review_detail/${this.reviewId}/`,
      headers: { Authorization: `JWT ${localStorage.getItem('jwt')}` }
    })
      .then(res => {
        this.reviewData = res.data
        console.log(this.reviewData)
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style>
.reviewbox {
  display: flex;
  flex-direction: column;
  justify-content: start;
}
.card-text{
  max-width: 90%;
  max-height: 80%;
  padding: 10px
}

.commentcreate-sizing {
  max-width: 100%;
  height: 40%;
}
.buttons {
  display: flex;
  justify-content: space-between; 
}

.white-bg {
  background-color: #ffffff;
}
.page-heading {
  border-top: 0;
  padding: 0 10px 20px 10px;
}

.ibox {
  clear: both;
  margin-bottom: 25px;
  margin-top: 0;
  padding: 0;
}
.ibox:after,
.ibox:before {
  display: table;
}
.ibox-title {
  -moz-border-bottom-colors: none;
  -moz-border-left-colors: none;
  -moz-border-right-colors: none;
  -moz-border-top-colors: none;
  background-color: #ffffff;
  border-color: #e7eaec;
  border-image: none;
  border-style: solid solid none;
  border-width: 3px 0 0;
  color: inherit;
  margin-bottom: 0;
  padding: 14px 15px 7px;
  min-height: 48px;
}
.ibox-content {
  border-radius: 20px;
  background-color: rgba(0,0,0,0.5);
  color: inherit;
  padding: 15px 20px 20px 20px;
  border-image: none;
  border-style: solid solid none;
  border-width: 1px 0;
}
.ibox-footer {
  color: inherit;
  border-top: 1px solid #e7eaec;
  font-size: 90%;
  background: #ffffff;
  padding: 10px 15px;
}

.message-input {
  height: 90px !important;
}
.form-control, .single-line {
  background-color: #FFFFFF;
  background-image: none;
  border: 1px solid #e5e6e7;
  border-radius: 1px;
  color: inherit;
  display: block;
  padding: 6px 12px;
  transition: border-color 0.15s ease-in-out 0s, box-shadow 0.15s ease-in-out 0s;
  width: 100%;
  font-size: 14px;
}
.text-navy {
  color: #1ab394;
}
.mid-icon {
  font-size: 66px !important;
}
.m-b-sm {
  margin-bottom: 10px;
}

.reviewmodified-sizing {
  width: 300px;
  height: 170px;
}



.container-sizing {
  padding: 24px;
}

.button-sizing {
  margin-top: 1rem;
  width: 140px;
  height: 45px;
}
</style>
