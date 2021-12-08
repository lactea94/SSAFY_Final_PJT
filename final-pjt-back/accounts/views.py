

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User

from .models import Profile
from .serializers import ProfileSerializer

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    if password != password_confirmation:
        return Response({'error' : '비밀번호가 일치하지 않습니다'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))

        profile = Profile()
        profile.content = ''
        profile.genre = ''
        profile.user = user
        profile.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({'error': '회원정보가 저장되지 않았습니다'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

#-----------------------프로필 관련 CRUD-----------------------------------------------------------#


@api_view(['GET'])
@permission_classes([AllowAny])
def profile_get(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'GET':
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def profile_update(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'PUT':
        if request.user == profile.user:
            
            profile.user = request.user
            genrelist = request.data['likeGenre']
            my_genre = ('/'.join(genrelist))
            profile.genre = my_genre
            profile.content = request.data['content']
            profile.save()


            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response({'Unauthorized': '권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN) 

