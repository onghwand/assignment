from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ledgers.models import Ledger

from datetime import datetime
'''
3-g. 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
'''
@api_view(['GET'])
def redirect_shorten_url(request, shorten_url):
    ledger = get_object_or_404(Ledger, shorten_url=shorten_url) 
    if ledger.expiration_time > datetime.now(): # 만료 여부 확인
        return HttpResponseRedirect(ledger.original_url)
    return Response({"message":"url 만료"}, status=status.HTTP_404_NOT_FOUND)