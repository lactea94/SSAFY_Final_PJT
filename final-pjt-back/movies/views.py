from django.db.models.expressions import Exists
from django.shortcuts import get_object_or_404
from .serializers import CommentSerializer, MovieSerializer, RecommendSerializer, ReviewSerializer, UserplaylistSerializer
from .models import Movie, Genre, Movielikeuser, Recommend, Review, Userplaylist, Comment
import sys
sys.path.append('/server/accounts')

from accounts.models import Profile, User

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
import requests

import json

# Create your views here.

#-----------------------------영화목록 생성--------------------------------------#
@api_view(['GET'])
@permission_classes([AllowAny])
def createmovielist(request):
    language = 'ko-kr'
    api_key = '539698afd330cbafe0612f13780904ef'

    
    baseurl = 'https://api.themoviedb.org/3/genre/movie/list'
    api_url = f'{baseurl}?api_key={api_key}&language={language}'
    response = requests.get(api_url).json()
    genre_list = response['genres']
    genres = Genre.objects.all()
    genres.delete()

    def get_genrecode(genre_list):
        for data in genre_list:
            genre = Genre()
            genre.genre_code = data['id']
            genre.genre_name = data['name']
            genre.save()
    
    get_genrecode(genre_list)

    #--------------------------------------------------------------------
    baseurl = 'https://api.themoviedb.org/3/movie/popular'
    movies = Movie.objects.all()
    movies.delete()
    id_index = 0

    for i in range(1, 50):
        page = i
        api_url = f'{baseurl}?api_key={api_key}&language={language}&page={page}'
        response = requests.get(api_url).json()
        results = response['results'] 

        def get_database(data, id_index):
            movie = Movie()
            movie.auto_increment_id = id_index
            try:
                movie.title = data['title']
            except:
                movie.title = 'unknown_movie_title'
            try:
                movie.overview = data['overview']
            except:
                movie.overview = 'unknown_movie_overview'
            try:
                if data['poster_path'] == None:
                    movie.poster_path = 'path'
                else:
                    movie.poster_path = data['poster_path']
            except:
                movie.poster_path = 'path'
            try:
                genre_code = data['genre_ids']
            except:
                genre_code = 'unknown_genre_code'

            genre_list = []
            for code in genre_code:
                res = Genre.objects.filter(genre_code=code).values('genre_name')[0]['genre_name']
                genre_list.append(res)
            movie.genre_code = genre_list

            try:
                movie.user_rating = data['vote_average']
            except:
                movie.user_rating = data['0']

            try:                
                movie.release_date = data['release_date']
            except:
                movie.release_date = '2000-01-01'
            movie.save()
        
        for movie in results:
            id_index += 1
            get_database(movie, id_index)

    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

#------------------------영화데이터 로드------------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def loadmovielist(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
#-----------------------추천영화 리스트----------------------------------------------------------#

@api_view(['GET'])
@permission_classes([AllowAny])
def logincreaterecommendlist(request):
    movies = Movie.objects.all()
    Recommend.objects.all().delete()
    
    profile = Profile.objects.get(user_id=request.user)
    print('ter1')
    genres = profile.genre
    my_genres = list(genres.split('/'))
    print('ter2')
    for movie in movies:
        str_object = movie.genre_code[2:-2]       
        dbmovie_genrelist = (str_object.split("', '"))
        cnt = 0
        for genre in my_genres:
            for genre_code in dbmovie_genrelist:
                if genre == genre_code:
                    cnt += 1
        
        if cnt >= 1:
            recommend = Recommend()
            try:
                recommend.title = movie.title
            except:
                recommend.title = 'Unknown_title'
            try:
                recommend.movie_pk = movie.auto_increment_id
            except:
                continue
            try:
                recommend.overview = movie.overview
            except:
                recommend.overview = 'Unknown_overview'
            try:
                recommend.poster_path = movie.poster_path
            except:
                recommend.poster_path = 'Unknown_poster_path'
            try:
                recommend.user_rating = movie.user_rating
            except:
                recommend.user_rating = 0
            try:
                recommend.release_date = movie.release_date
            except:
                recommend.release_date = '2000-01-01'
            try:
                recommend.priority = cnt
            except:
                recommend.priority = 0
            try:
                recommend.save()
            except:
                print(recommend)
    movies = Recommend.objects.all().order_by('-priority', '-user_rating')[:30]
    if len(movies) > 10:
        serializer = RecommendSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        Recommend.objects.all().delete()
        movies = Movie.objects.all().order_by('-user_rating')[:30]

        for movie in movies:
            recommend = Recommend()
            recommend.title = movie.title
            recommend.movie_pk = movie.auto_increment_id
            recommend.overview = movie.overview
            recommend.poster_path = movie.poster_path
            recommend.release_date = movie.release_date
            recommend.user_rating = movie.user_rating
            recommend.priority = 0
            recommend.save()

        recommends = Recommend.objects.all()
        serializer = RecommendSerializer(recommends, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes([AllowAny])
def logoutcreaterecommendlist(request):
    Recommend.objects.all().delete()
    movies = Movie.objects.all().order_by('-user_rating')[:30]

    for movie in movies:
        recommend = Recommend()
        recommend.title = movie.title
        recommend.movie_pk = movie.auto_increment_id
        recommend.overview = movie.overview
        recommend.poster_path = movie.poster_path
        recommend.release_date = movie.release_date
        recommend.user_rating = movie.user_rating
        recommend.priority = 0
        recommend.save()

    recommends = Recommend.objects.all()
    serializer = RecommendSerializer(recommends, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

#-----------------------단일영화정보 + 리뷰---------------------------------------------------------#
@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, movie_pk):
    if request.method == 'GET':
        
        movie = Movie.objects.get(pk = movie_pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_search(request, searchvalue):
    movies = Movie.objects.filter(title__contains=searchvalue)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes([AllowAny])
def review_list(request, movie_pk):
    if request.method == 'GET':
        reviews = Review.objects.filter(movie=movie_pk).order_by('-pk')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def review_detail(request, review_pk):
    if request.method =='GET':
        review = get_object_or_404(Review, review_pk=review_pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def review_create(request, movie_pk):
    user = request.user
    movie = Movie.objects.get(pk=movie_pk)

    if request.method == 'POST':   
        review = Review()
        review.movie = movie
        review.user = request.user
        review.username = user.username
        review.content = request.data['content']
        review.save()

        serializer = ReviewSerializer(review)        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_update_delete(request, movie_pk, review_pk):
    
    review = get_object_or_404(Review, movie = movie_pk, review_pk = review_pk)
    if request.user == review.user:

        if request.method == 'DELETE':
            review.delete()
            data = {
                'delete' : f'{review_pk}번 리뷰가 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)

        elif request.method == 'PUT':
                review = get_object_or_404(Review, movie=movie_pk, review_pk=review_pk)
                review.content = request.data['reviewItem']['content']
                review.save()
                serializer = ReviewSerializer(review)
                return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({'Unauthorized': '권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)

#-----------------------플레이리스트 CRUD---------------------------------------------------------#
@api_view(['GET'])
@permission_classes([AllowAny])
def get_userplaylist(request):
    if request.method == 'GET':
        alluser = User.objects.all()
        serializer = {}
        for user in alluser:
            try:
                query = Userplaylist.objects.filter(user_id=user.pk)
                serializer[str(user.username)] = [query[0].p_title, query[0].p_content]
                movie_id_list = []
                for q in query:
                    movie_id_list.append(q.movie_id)
                serializer[str(user.username)].append(movie_id_list)
            except:
                pass
        return Response(serializer)

@api_view(['GET'])
@permission_classes([AllowAny])
def userplaylist_get_movies(request, movielist):

    movielist = list(movielist.split('-'))    
    
    serializer = {}
    i = 0
    for movie_pk in movielist:
        i += 1
        movie = Movie.objects.get(auto_increment_id = movie_pk)
        serializer[f'movie{i}'] = MovieSerializer(movie).data
    return Response(serializer, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def add_userplaylist(request):
    if request.method =='POST':
        #Userplaylist.objects.filter(user=request.user).delete()

        exist_title_list = []
        if Userplaylist.objects.filter(user=request.user).exists():
            user_playlist = Userplaylist.objects.filter(user=request.user)
            for movie in user_playlist:
                exist_title_list.append(movie.movie_title)
        
        for movie_title in request.data['introduce']['movielist']:
            print(movie_title)
            movie = Movie.objects.filter(title=movie_title)[0]
            if not  movie.title in exist_title_list: 
                playlist = Userplaylist()
                playlist.user = request.user
                playlist.movie = movie
                playlist.movie_title = movie.title
                playlist.p_title = request.data['introduce']['title']
                playlist.p_content = request.data['introduce']['content']
                playlist.poster_path = movie.poster_path
                playlist.overview = movie.overview
                playlist.save()
        
        playlist = Userplaylist.objects.filter(user=request.user)
        serializer = UserplaylistSerializer(playlist, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def userplaylist_update_delete(request, user_pk, movie_pk):
    playlist = get_object_or_404(Userplaylist, user = user_pk, movie = movie_pk)

    if request.user == playlist.user:
        if request.method == 'DELETE':
            playlist.delete()
            data = {
                'delete' : f'{playlist.pk}번 리스트가 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        
        elif request.method == 'PUT':
            serializer = ReviewSerializer(playlist, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    return Response({'Unauthorized': '권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)

#--------------------------코멘트 관련 CRUD------------------------------------------------#
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def commentlist_or_create(request, review_pk):
    if request.method == 'GET':
        comments = Comment.objects.filter(review_id=review_pk).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        review = Review.objects.get(review_pk=review_pk)
        comment = Comment()
        comment.review = review
        comment.content = request.data['content']
        try:
            user = request.user
            comment.user = request.user
            comment.username = user.username
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def commentupdate_or_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, review=review_pk, pk=comment_pk)
    if request.method == 'PUT':
        if request.user == comment.user:

            comment.content = request.data['commentItem']['content']
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

    if request.method == 'DELETE':
        if request.user == comment.user:
            comment.delete()
            comments = Comment.objects.filter(review=review_pk)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({'Unauthorized': '권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)

#-----------LIKE----------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def logout_get_movie_like(request, movie_pk):
    movie = Movie.objects.get(auto_increment_id = movie_pk)
    print(request.user)
    data = 'dislike'
    Movielikeuser.objects.filter(movie = movie_pk)
    likenumber = movie.liked_number
    return Response({'data': data, 'likenumber': likenumber}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def login_get_movie_like(request, movie_pk):
    print('1')
    print('2')
    movie = Movie.objects.get(auto_increment_id = movie_pk)

    if Movielikeuser.objects.filter(movie = movie_pk, user = request.user).exists():
        data = 'like'
    else:
        data = 'dislike'

    likenumber = movie.liked_number
    return Response({'data': data, 'likenumber': likenumber}, status=status.HTTP_200_OK)
    



@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def update_movie_like(request, movie_pk):
    if Movielikeuser.objects.filter(movie=movie_pk).filter(user=request.user).exists():
        like = get_object_or_404(Movielikeuser, movie=movie_pk, user=request.user)
        like.delete()

        movie = Movie.objects.get(auto_increment_id = movie_pk)
        movie.liked_number -= 1
        movie.save()

        total_number = movie.liked_number
        return Response({'data': 'dislike', 'likenumber': total_number}, status=status.HTTP_202_ACCEPTED)

    else:
        movie = get_object_or_404(Movie, auto_increment_id=movie_pk)
        instance = Movielikeuser()
        instance.movie = movie
        instance.user = request.user
        instance.save()

        movie = Movie.objects.get(auto_increment_id = movie_pk)
        movie.liked_number += 1
        movie.save()

        total_number = movie.liked_number
        return Response({'data': 'like', 'likenumber': total_number}, status=status.HTTP_202_ACCEPTED) 
