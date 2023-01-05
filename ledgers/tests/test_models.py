from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError

from ledgers.models import Ledger
from accounts.models import User

class LedgersModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(email="pay@here.com", password="payhere") 
        Ledger.objects.create(user=user, memo="hi", cashflow=100, year=2023, month=1, day=6)

    def test_user_label(self):
        field_label = Ledger._meta.get_field("user").verbose_name
        self.assertEquals(field_label, "user")
    
    def test_memo_max_length(self):
        max_length = Ledger._meta.get_field("memo").max_length
        self.assertEquals(max_length, 256)

    def test_memo_null_true(self):
        null = Ledger._meta.get_field("memo").null
        self.assertTrue(null)

    # def test_min_of_month(self):
    #     user = User.objects.create_user(email="pay1@here.com", password="payhere")
    #     self.assertRaises(ValidationError, Ledger.objects.create, user=user, memo="hi", cashflow=100, year=2023, month=0, day=6)

    # def test_user_on_delete_CASCADE(self):
    #     ledger=Ledger.objects.get(id=1)
    #     ledger.user.delete()
    #     self.assertRaises(ObjectDoesNotExist, Ledger.objects.get(id=1))
    