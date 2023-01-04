from django.db import models
from django.conf import settings

# Create your models here.
class Ledger(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ledgers")
    memo = models.CharField(max_length=256, null=True)
    cashflow = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    url = models.CharField(max_length=256, null=True)
    