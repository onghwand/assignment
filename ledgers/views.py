from django.shortcuts import get_list_or_404, get_object_or_404
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Ledger
from .serializers import LedgerListSerializer, LedgerSerializer

from hashlib import sha256
from datetime import datetime, timedelta

# Create your views here.
'''
3-a. 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
3-d. 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다. 
'''
@api_view(["GET", "POST"])
def ledger_list_or_create(request, user_pk):
    def ledger_list():
        ledgers = get_list_or_404(Ledger.objects.order_by("-year","-month","-day"), user=user_pk)
        serializer = LedgerListSerializer(ledgers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_ledger():
        serializer = LedgerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({"message": "생성 완료"}, status=status.HTTP_201_CREATED)

    # 가계부 주인 여부 확인
    if request.user.pk == user_pk:
        if request.method == "GET":
            return ledger_list()
        elif request.method == "POST":
            return create_ledger()
    return Response({"message": "권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)


'''
3-b. 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다. 
3-c. 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다. 
3-e. 가계부에서 상세한 세부 내역을 볼 수 있습니다.
'''
@api_view(["GET", "PATCH", "DELETE"])
def ledger_read_or_update_or_delete(request, ledger_pk):
    ledger = get_object_or_404(Ledger, pk=ledger_pk)

    def read():
        serializer = LedgerSerializer(ledger)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update():       
        serializer = LedgerSerializer(instance=ledger, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "수정 완료"}, status=status.HTTP_204_NO_CONTENT)
        
    def delete():
        ledger.delete()
        return Response({"message": "삭제 완료"}, status=status.HTTP_204_NO_CONTENT)

    # 가계부의 주인인 경우에만 권한 부여  
    if request.user == ledger.user:
        if request.method == "GET":
            return read()
        elif request.method == "PATCH":
            return update()
        elif request.method == "DELETE":
            return delete()
    return Response({"message": "권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
    


'''
3-f. 가계부의 세부 내역을 복제할 수 있습니다.
'''
@api_view(["GET"])
def ledger_duplicate(request, ledger_pk):
    ledger = get_object_or_404(Ledger, pk=ledger_pk)

    # 가계부의 주인인 경우에만 복제 권한 부여
    if request.user == ledger.user:
        # 가계부 복제
        ledger.pk = None
        ledger.save()
        return Response({"message": "생성 완료"}, status=status.HTTP_201_CREATED)
    return Response({"message": "권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)
    


'''
3-g. 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
'''
@api_view(["POST"])
def make_shorten_url(request, ledger_pk):
    # 단축 url 제한 시간
    TIME_LIMIT = timedelta(minutes=10)
    ledger = get_object_or_404(Ledger, pk=ledger_pk)
    
    # 가계부의 주인인 경우에만 권한 부여
    if request.user == ledger.user:
        original_url = request.data["url"] # 프론트에서 보낸 장문의 url이라고 가정
        present, expiration_time = datetime.now(), datetime.now()+TIME_LIMIT
        # 현재 시간을 같이 암호화한 이유는 다른 사람이 외워서 접속하는 것을 방지하기 위함
        shorten_url = sha256(original_url.encode()+str(present).encode()).hexdigest()[:8] 
        
        # DB 반영
        ledger.original_url = original_url
        ledger.shorten_url = shorten_url
        ledger.expiration_time = expiration_time
        ledger.save()
        return Response({"shorten_url": settings.SITE_URL+shorten_url}, status=status.HTTP_201_CREATED)
    return Response({"message": "권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)

