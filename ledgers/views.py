from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
'''
3-a. 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다.
3-d. 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다. 
'''
@api_view(["GET", "POST"])
def ledger_list_or_create(request):
    pass


'''
3-b. 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다. 
3-c. 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다. 
3-e. 가계부에서 상세한 세부 내역을 볼 수 있습니다.
'''
@api_view(["GET","UPDATE","DELETE"])
def ledger_read_or_update_or_delete(request):
    pass


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


