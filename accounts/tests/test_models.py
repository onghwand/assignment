from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from accounts.models import User

class AccountsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create_user(email="pay@here.com", password="payhere")

    def test_email_label(self):
        field_label = User._meta.get_field("email").verbose_name
        self.assertEquals(field_label, "email")
    
    def test_email_max_length(self):
        max_length = User._meta.get_field("email").max_length
        self.assertEquals(max_length, 30)

    def test_object_name_is_email(self):
        user = User.objects.get(id=1)
        expected_object_name = user.email
        self.assertEquals(expected_object_name, str(user))
    
    def test_default_of_is_superuser_is_false(self):
        user = User.objects.get(id=1)
        is_superuser = user.is_superuser
        self.assertFalse(is_superuser)
    
    def test_email_raise_value_error(self):
        self.assertRaises(ValueError, User.objects.create_user, email="", password="payhere")
    
    def test_unique_of_email(self):
        self.assertRaises(IntegrityError, User.objects.create_user, email="pay@here.com", password="payhere")
    
    # def test_unique_of_email(self):
    #     self.assertRaises(ValidationError, User.objects.create_user, email=" ", password="payhere")
        