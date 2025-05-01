from django.urls import path
from . import views

app_name = 'trading'

urlpatterns = [
    path('', views.trading_dashboard, name='dashboard'),
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/<int:account_id>/', views.account_detail, name='account_detail'),
    path('trades/', views.trade_list, name='trade_list'),
]