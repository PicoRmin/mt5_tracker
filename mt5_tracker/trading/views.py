from django.shortcuts import render, get_object_or_404
from .models import MT5Account, Trade

def trading_dashboard(request):
    return render(request, 'trading/dashboard.html')

def account_list(request):
    accounts = MT5Account.objects.all()
    return render(request, 'trading/account_list.html', {'accounts': accounts})

def account_detail(request, account_id):
    account = get_object_or_404(MT5Account, id=account_id)
    trades = account.trades.all()
    return render(request, 'trading/account_detail.html', {'account': account, 'trades': trades})

def trade_list(request):
    trades = Trade.objects.all()
    return render(request, 'trading/trade_list.html', {'trades': trades})