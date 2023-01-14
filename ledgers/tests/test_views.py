from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from ledgers.models import Ledger

# from unittest import mock
from datetime import datetime, timedelta
from freezegun import freeze_time

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
    def test_ledger_list(self):
        response = self.client.post(reverse("accounts:login"),{"email":"pay@here.com", "password":"payhere"})
        user_pk = response.data["user"]["id"]
        token = response.data["token"]["access"]
        response = self.client.get(reverse("ledgers:list_or_create", kwargs={"user_pk":user_pk}), **{"HTTP_AUTHORIZATION": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

        # jwt 없으면 401
        response = self.client.get(reverse("ledgers:list_or_create", kwargs={"user_pk":user_pk}))
        self.assertEqual(response.status_code, 401)

        # 다른 사람 것 조회 불가
        response = self.client.post(reverse("accounts:login"),{"email":"pay1@here.com", "password":"payhere"})
        user_pk = response.data["user"]["id"]
        response = self.client.get(reverse("ledgers:list_or_create", kwargs={"user_pk":user_pk}), **{"HTTP_AUTHORIZATION": f"Bearer {token}"})
        self.assertEqual(response.status_code, 401)

    # 가계부 생성
    def test_create_ledger(self):
        response = self.client.post(reverse("accounts:login"),{"email":"pay@here.com", "password":"payhere"})
        user_pk = response.data["user"]["id"]
        token = response.data["token"]["access"]
        data = {"memo": "test1", "cashflow": 100, "year": 2023, "month": 12, "day": 4}
        response = self.client.post(reverse("ledgers:list_or_create", kwargs={"user_pk":user_pk}), data=data, **{"HTTP_AUTHORIZATION": f"Bearer {token}"})
        self.assertEqual(response.status_code, 201) 

        # jwt 없으면 401
        response = self.client.post(reverse("ledgers:list_or_create", kwargs={"user_pk":user_pk}), data=data)
        self.assertEqual(response.status_code, 401)

    # 가계부 수정
    def test_update_ledger(self):
        token = self.client.post(reverse("accounts:login"),{"email":"pay@here.com", "password":"payhere"}).data["token"]["access"]
        ledger = Ledger.objects.get(memo="pay1")
        self.assertEqual(ledger.cashflow, 100)

        data = {"cashflow": 2000}
        # 왜 patch는 content_type을 지정해야만 하나
        response = self.client.patch(reverse("ledgers:read_or_update_or_delete", kwargs={"ledger_pk":ledger.pk}), data=data, **{"HTTP_AUTHORIZATION": f"Bearer {token}"}, content_type="application/json")
        self.assertEqual(response.status_code, 204)

        # 수정 반영 확인
        ledger = Ledger.objects.get(memo="pay1")
        self.assertEqual(ledger.cashflow, 2000) 

    # 가계부 삭제
    def test_delete_ledger(self):
        token = self.client.post(reverse("accounts:login"),{"email":"pay@here.com", "password":"payhere"}).data["token"]["access"]
        ledger = Ledger.objects.get(memo="pay1")

        response = self.client.delete(reverse("ledgers:read_or_update_or_delete", kwargs={"ledger_pk":ledger.pk}), **{"HTTP_AUTHORIZATION": f"Bearer {token}"})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Ledger.objects.filter(memo="pay1").count(), 0)

    # 가계부 상세정보 조회
    def test_ledger_detail(self):
        token = self.client.post(reverse("accounts:login"),{"email":"pay@here.com", "password":"payhere"}).data["token"]["access"]
        ledger = Ledger.objects.get(memo="pay1")
        response = self.client.get(f"/api/v1/ledgers/{ledger.pk}/detail/", **{"HTTP_AUTHORIZATION": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
    
        # reverse 사용
        ledger = Ledger.objects.get(memo="pay1")
        response = self.client.get(reverse("ledgers:read_or_update_or_delete", kwargs={"ledger_pk":ledger.pk}), **{"HTTP_AUTHORIZATION": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)

    # 가계부 복제
    def test_duplicate_ledger(self):
        token = self.client.post(reverse("accounts:login"),{"email":"pay@here.com", "password":"payhere"}).data["token"]["access"]
        ledger = Ledger.objects.get(memo="pay1")

        response = self.client.get(reverse("ledgers:duplicate", kwargs={"ledger_pk":ledger.pk}), **{"HTTP_AUTHORIZATION": f"Bearer {token}"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ledger.objects.filter(memo="pay1").count(), 2)

    # 가계부 단축 url (생성, 만료시간) 
    # => 생성과 만료시간 테스트를 분리하는게 좋은건지, view의 TIME_LIMIT 변수 밖으로 빼서 가져오는게 좋은건지
    def test_expiration_time_of_shorten_url(self):
        created_at = datetime(2023, 1, 14, 17, 23, 10) # 단축 url 생성 시간
        still_active_at = created_at + timedelta(minutes=9, seconds=59) # 만료 직전(1초전)
        expired_at = created_at + timedelta(minutes=10) # 만료 시점

        with freeze_time(created_at) as frozen_datetime:
            # 단축 url 생성
            token = self.client.post(reverse("accounts:login"),{"email":"pay@here.com", "password":"payhere"}).data["token"]["access"]
            ledger = Ledger.objects.get(memo="pay1")
            data = {"url": "https://payhere.in/"}

            # 생성 확인
            response = self.client.post(reverse("ledgers:shorten_url", kwargs={"ledger_pk":ledger.pk}), data=data, **{"HTTP_AUTHORIZATION": f"Bearer {token}"})
            self.assertEqual(response.status_code, 201)

            # 단축 url 생성 직후 연결 확인
            ledger = Ledger.objects.get(memo="pay1")
            response = self.client.get(reverse("redirect_shorten_url", kwargs={"shorten_url":ledger.shorten_url}))
            self.assertEqual(response.status_code, 302)

            # 만료시간 테스트

            # 9분 59초는 302
            frozen_datetime.move_to(still_active_at)
            response = self.client.get(reverse("redirect_shorten_url", kwargs={"shorten_url":ledger.shorten_url}))
            self.assertEqual(response.status_code, 302)
            # 10분은 404
            frozen_datetime.move_to(expired_at)
            response = self.client.get(reverse("redirect_shorten_url", kwargs={"shorten_url":ledger.shorten_url}))
            self.assertEqual(response.status_code, 404)


        
            

        