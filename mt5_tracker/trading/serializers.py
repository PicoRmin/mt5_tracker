from rest_framework import serializers
from trading.models import MT5Account

class MT5AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MT5Account
        fields = ['account_id', 'broker', 'created_at']