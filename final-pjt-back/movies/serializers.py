from rest_framework import serializers
from .models import Genre, Movie, Movielikeuser, Recommend, Review, Userplaylist, Comment


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('genre_code', 'genre_name',)

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

class UserplaylistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Userplaylist
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

class RecommendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recommend
        fields = '__all__'

class MovielikeuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movielikeuser
        fields = '__all__'