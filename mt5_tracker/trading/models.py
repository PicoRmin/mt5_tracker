from django.db import models

# Create your models here.
from accounts.models import User

class MT5Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.IntegerField(unique=True)
    broker = models.CharField(max_length=100)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'trading'  # این خط را اضافه کنید
        verbose_name = 'MT5 Account'
        verbose_name_plural = 'MT5 Accounts'

    def __str__(self):
        return f"{self.account_id} ({self.broker})"

class Trade(models.Model):
    account = models.ForeignKey(MT5Account, on_delete=models.CASCADE, related_name='trades')
    ticket_id = models.IntegerField()
    symbol = models.CharField(max_length=20)
    type = models.CharField(max_length=10)  # BUY/SELL
    volume = models.FloatField()
    entry_price = models.FloatField()
    exit_price = models.FloatField()
    profit = models.FloatField()
    swap = models.FloatField()
    commission = models.FloatField()
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField()
    duration = models.DurationField()
    magic_number = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    
    class Meta:
        app_label = 'trading'  # این خط را اضافه کنید