from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from accounts import views

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email="pay@here.com", password="payhere")

    def test_login(self):
        pass

    