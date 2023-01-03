from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

'''
작성자: 이동환
설명: 기본 테스트
'''
@api_view(['GET'])
def test(request):
    return Response({'hello':'world'})