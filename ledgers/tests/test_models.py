from django.test import TestCase
from django.core.exceptions import ValidationError

from ledgers.models import Ledger
from accounts.models import User

class LedgersModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(email="pay@here.com", password="payhere") 
        Ledger.objects.create(user=user, memo="hi", cashflow=100, year=2023, month=1, day=6)

    # 유저 label 
    def test_user_label(self):
        field_label = Ledger._meta.get_field("user").verbose_name
        self.assertEqual(field_label, "user")
    
    # memo 최대 길이
    def test_memo_max_length(self):
        max_length = Ledger._meta.get_field("memo").max_length
        self.assertEqual(max_length, 256)

    # memo null 가능
    def test_memo_null_is_true(self):
        null = Ledger._meta.get_field("memo").null
        self.assertTrue(null)

    # month 최솟값 1(월)
    def test_min_of_month(self):
        ledger = Ledger.objects.get(id=1)
        ledger.month = 0
        self.assertRaises(ValidationError, ledger.full_clean)

    # 유저 삭제에 따른 가계부 삭제
    def test_user_on_delete_CASCADE(self):
        ledger=Ledger.objects.get(id=1)
        ledger.user.delete()
        self.assertEqual(Ledger.objects.all().count(), 0)
    