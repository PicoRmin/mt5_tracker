from django.urls import path
from . import views

urlpatterns = [
    path('test-connection/', views.test_connection, name='test_connection'),
    path('register-account/', views.register_account, name='register_account'),
    path('upload-trade/', views.upload_trade, name='upload_trade'),
]