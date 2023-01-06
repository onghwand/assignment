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
        response= self.client.post(reverse("accounts:login"),{"email":"pay@here.com", "password":"payhere"})
        self.assertEqual(response.status_code, 200)

        response= self.client.post(reverse("accounts:login"),{"email":"pay1@here.com", "password":"payhere"})
        self.assertEqual(response.status_code, 400)
    
    # 로그아웃
    def test_logout(self):
        response = self.client.post(reverse("accounts:login"),{"email":"pay@here.com", "password":"payhere"})
        self.assertTrue('token' in response.data)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.delete(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 204)
        