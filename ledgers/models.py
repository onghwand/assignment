from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Ledger(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ledgers")
    memo = models.CharField(max_length=256, null=True)
    cashflow = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    original_url = models.CharField(max_length=256, null=True)
    shorten_url = models.CharField(max_length=256, null=True)
    expiration_time = models.DateTimeField(null=True)
    