from django.contrib import admin
from .models import Currency, ExchangeRate, UserProfile, Trade, APICall

admin.site.register(Currency)
admin.site.register(ExchangeRate)
admin.site.register(UserProfile)
admin.site.register(Trade)
admin.site.register(APICall)
