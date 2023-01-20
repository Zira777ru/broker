from django.db import models
from django.contrib.auth.models import User




class Currency(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3)
    symbol = models.CharField(max_length=10)

class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchange_rate_from_currency')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchange_rate_to_currency')
    rate = models.DecimalField(max_digits=10, decimal_places=2)

class TradingPair(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='trading_pair_from_currency')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='trading_pair_to_currency')
    price = models.DecimalField(max_digits=10, decimal_places=2)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Leverage(models.Model):
    value = models.DecimalField(max_digits=2, decimal_places=1)

class Trade(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    trading_pair = models.ForeignKey(TradingPair, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    is_open = models.BooleanField(default=True)
    leverage = models.ForeignKey(Leverage, on_delete=models.SET_NULL, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    take_profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class APICall(models.Model):
    date_time = models.DateTimeField()
    parameters = models.TextField()
    response = models.TextField()


