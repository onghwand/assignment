from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import *

# Create your views here.

'''

설명: 기본 테스트
'''
@api_view(["GET"])
def test(request):
    return Response({"hello":"world"})

'''
회원가입
'''
@api_view(["POST"])
def signup(request):
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
            status=status.HTTP_201_CREATED
        )

        # jwt 토큰 쿠키 저장(httponly => js로 조회 x)
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)
        return res
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
로그인
'''
@api_view(["POST"])
def login(request):
    # 유저 인증
    user = authenticate(
        email=request.data.get("email"), password=request.data.get("password")
    )
    # 유저 존재
    if user is not None:
        serializer = UserSerializer(user)
        # jwt 토큰
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        response = Response(
            {
                "user": serializer.data,
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie("access", access_token, httponly=True)
        response.set_cookie("refresh", refresh_token, httponly=True)
        return response
    # 유저 존재 x
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

'''
로그아웃
'''
@api_view(["DELETE"])
def logout(request):
    # 로그인상태 확인할 필요 있는지 찾아보기
    # 쿠키에 저장된 토큰 삭제
    response = Response(status=status.HTTP_204_NO_CONTENT)
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    return response
    
    