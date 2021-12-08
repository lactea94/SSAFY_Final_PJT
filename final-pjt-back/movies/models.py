from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField


# Create your models here.

class Movie(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45)
    overview = models.TextField(max_length=300)
    poster_path = models.CharField(max_length=200, default='/path.jpg')
    user_rating = models.IntegerField()
    genre_code = models.CharField(max_length=50)
    release_date = models.CharField(max_length=20)
    liked_number = models.IntegerField(default='0')

class Genre(models.Model):
    genre_code = models.IntegerField()
    genre_name = models.CharField(max_length=50)

class Review(models.Model):
    review_pk = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    movie = models.ForeignKey(Movie, on_delete=CASCADE)
    content = models.TextField()
    class Rank(models.IntegerChoices):
        fantastic = 5
        great = 4
        normal = 3
        terrible = 2
        garbage = 1
    username = models.CharField(max_length=100)
    rank = models.IntegerField(choices=Rank.choices, default=Rank.normal)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Userplaylist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    movie = models.ForeignKey(Movie, on_delete=CASCADE)
    p_title = models.CharField(max_length=100)
    p_content = models.TextField()
    movie_title = models.CharField(max_length=500)
    
class Comment(models.Model):
    comment_pk = models.AutoField(primary_key=True)
    review = models.ForeignKey(Review, on_delete=CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    content = models.TextField() 
    username = models.CharField(max_length=100, default='unknown')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Recommend(models.Model):
    title = models.CharField(max_length=45)
    movie_pk = models.IntegerField()
    overview = models.TextField(max_length=300)
    poster_path = models.CharField(max_length=200, default='path')
    user_rating = models.IntegerField()
    release_date = models.CharField(max_length=20)
    priority = models.IntegerField()

class Movielikeuser(models.Model):
    movie = models.ForeignKey(Movie, on_delete=CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)