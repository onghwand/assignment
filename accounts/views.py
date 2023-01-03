from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import *

# Create your views here.

'''
작성자: 이동환
설명: 기본 테스트
'''
@api_view(['GET'])
def test(request):
    return Response({'hello':'world'})

'''
작성자: 이동환
설명: 회원가입
'''
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # jwt
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        res = Response(
            {
                "user": serializer.data,
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_200_OK
        )

        # jwt 토큰 쿠키 저장(httponly => js로 조회 x)
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)
        return res
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    return 