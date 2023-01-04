from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Ledger

User = get_user_model()

class LedgerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        fields = ("pk","cashflow","year","month","day",)

class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        exclude = ("user","original_url","shorten_url","expiration_time",)