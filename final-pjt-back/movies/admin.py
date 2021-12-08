from django.contrib import admin
from .models import Genre, Movie, Comment, Review

class GenreAdmin(admin.ModelAdmin):   
    list_display = ['genre_code', 'genre_name']

class MovieAdmin(admin.ModelAdmin):
    list_display = ['auto_increment_id', 'title', 'user_rating', 'genre_code', 'release_date']
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review_pk', 'user', 'movie', 'content', 'rank', 'created_at', 'updated_at']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_pk', 'review', 'user', 'content', 'created_at', 'updated_at']


admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
