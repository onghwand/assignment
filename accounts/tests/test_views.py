from django.test import TestCase
from django.urls import reverse

from accounts.models import User

class AccountsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email="pay@here.com", password="payhere")

    # 회원가입
    def test_signup(self):
        response = self.client.post(reverse("accounts:signup"),{"email":"pay1@here.com", "password":"payhere"})
        self.assertEqual(response.status_code, 201)

    # 로그인 
    def test_login(self):
        response_200 = self.client.post(reverse("accounts:login"),{"email":"pay@here.com", "password":"payhere"})
        response_400 = self.client.post(reverse("accounts:login"),{"email":"pay1@here.com", "password":"payhere"})
        self.assertEqual(response_200.status_code, 200)
        self.assertEqual(response_400.status_code, 400)
    
    # 로그아웃
    def test_logout(self):
        response_200 = self.client.post(reverse("accounts:login"),{"email":"pay@here.com", "password":"payhere"})
        self.assertEqual(response_200.status_code, 200)
        response_204 = self.client.delete(reverse("accounts:logout"))
        self.assertEqual(response_204.status_code, 204)
        # print(len(self.client.cookies["access"]))
        # self.assertTrue(len(self.client.cookies["access"]) == 0)