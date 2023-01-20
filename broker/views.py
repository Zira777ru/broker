import requests
from datetime import datetime
from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import ExchangeRate, Currency, UserProfile, Trade, APICall

@login_required
def exchange_rate(request):
    if request.method == 'POST':
        from_currency = request.POST['from_currency']
        to_currency = request.POST['to_currency']

        # Make an API call to ALPHA Vantage to get the exchange rate
        api_key = 'WYDLCMWS61R2VF8M'
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()

        # Extract the exchange rate from the API response
        exchange_rate = data['Realtime Currency Exchange Rate']['5. Exchange Rate']

        # Save the exchange rate and API call information to the database
        rate = ExchangeRate.objects.create(rate=exchange_rate, date_time=datetime.now(),
                                           from_currency=Currency.objects.get(code=from_currency),
                                           to_currency=Currency.objects.get(code=to_currency))
        APICall.objects.create(date_time=datetime.now(), parameters=url, response=response.text)
        context = {'exchange_rate': exchange_rate}
        return render(request, 'broker/exchange_rate.html', context)
    else:
        currencies = Currency.objects.all()
        context = {'currencies': currencies}
        return render(request, 'broker/exchange_rate.html', context)

@login_required
def trade(request):
    try:
        user = request.user.userprofile
    except UserProfile.DoesNotExist:
        user = UserProfile.objects.create(user=request.user)
    if request.method == 'POST':
        exchange_rate_id = request.POST['exchange_rate']
        amount = Decimal(request.POST.get('amount', 0))

        # Update the user's balance
        exchange_rate = ExchangeRate.objects.get(id=exchange_rate_id)
        user.balance -= exchange_rate.rate * amount
        user.save()

        # Create a new trade
        trade = Trade.objects.create(user=user, exchange_rate=exchange_rate, amount=amount, date_time=datetime.now())
        context = {'trade': trade}
        return render(request, 'broker/trade.html', context)
    else:
        exchange_rates = ExchangeRate.objects.all()
        context = {'exchange_rates': exchange_rates}
        return render(request, 'broker/trade.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('exchange_rate')
        else:
            context = {'error': 'Invalid login credentials'}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')