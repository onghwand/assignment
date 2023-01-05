from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from ledgers.models import Ledger

class LedgersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls): 
        user1 = User.objects.create_user(email="pay@here.com", password="payhere")
        user2 = User.objects.create_user(email="pay1@here.com", password="payhere")

        number_of_ledgers = 10
        for ledger_id in range(number_of_ledgers):
            Ledger.objects.create(user=user1, memo=f"pay{ledger_id}", cashflow=100, year=2023, month=1, day=6)
            Ledger.objects.create(user=user2, memo=f"here{ledger_id}", cashflow=200, year=2023, month=1, day=2)

    # 가계부 리스트 조회

    # 가계부 생성

    # 가계부 수정

    # 가계부 삭제

    # 가계부 상세정보 조회

    # 가계부 복제

    # 가계부 단축 url