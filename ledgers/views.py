from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Ledger
from .serializers import LedgerListSerializer, LedgerSerializer
# Create your views here.
'''
3-a. 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
3-d. 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다. 
'''
@api_view(["GET", "POST"])
def ledger_list_or_create(request, user_pk):
    def ledger_list():
        ledgers = get_list_or_404(Ledger, user=user_pk)
        serializer = LedgerListSerializer(ledgers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_ledger():
        serializer = LedgerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({"message": "생성 완료"}, status=status.HTTP_201_CREATED)

    # 로그인 여부 확인하기

    if request.method == "GET":
        return ledger_list()
    elif request.method == "POST":
        return create_ledger()


'''
3-b. 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다. 
3-c. 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다. 
3-e. 가계부에서 상세한 세부 내역을 볼 수 있습니다.
'''
@api_view(["GET","PATCH","DELETE"])
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

    # 가계부의 주인인 경우에만 조회/수정/삭제 권한 부여
    if request.user == ledger.user:
        if request.method == "GET":
            return read()
        elif request.method == "PATCH":
            return update()
        elif request.method == "DELETE":
            return delete()
    else:
        return Response({"message": "권한 없음"}, status=status.HTTP_401_UNAUTHORIZED)


'''
3-f. 가계부의 세부 내역을 복제할 수 있습니다.
'''
@api_view(["GET"])
def ledger_duplicate(request):
    pass


'''
3-g. 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
'''
@api_view(["GET"])
def ledger_url(request):
    pass


