from django.urls import path
from . import views

urlpatterns = [
    path('createmovielist/', views.createmovielist),
    path('loadmovielist/', views.loadmovielist),
    path('search/<str:searchvalue>/', views.movie_search),


    path('detail/<int:movie_pk>/', views.movie_detail),

    path('review_list/<int:movie_pk>/', views.review_list),
    path('review_detail/<int:review_pk>/', views.review_detail),
    path('review_create/<int:movie_pk>/', views.review_create),
    path('review_update_delete/<int:movie_pk>/<int:review_pk>/', views.review_update_delete),

    path('userplaylist/', views.get_userplaylist),
    path('userplaylist/add/', views.add_userplaylist),
    path('userplaylist/<int:user_pk>/<int:movie_pk>/', views.userplaylist_update_delete),
    path('userplaylist/movies/<str:movielist>/', views.userplaylist_get_movies),

    path('commentlist_or_create/<int:review_pk>/', views.commentlist_or_create),
    path('commentupdate_or_delete/<int:review_pk>/<int:comment_pk>/', views.commentupdate_or_delete),

    path('loginrecommendmovielist/', views.logincreaterecommendlist),
    path('logoutrecommendmovielist/', views.logoutcreaterecommendlist),
    
    path('logout_get_movie_like/<int:movie_pk>/', views.logout_get_movie_like),
    path('login_get_movie_like/<int:movie_pk>/', views.login_get_movie_like),

    path('movie_like/<int:movie_pk>/', views.update_movie_like)
]