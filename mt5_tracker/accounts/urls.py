from django.urls import path
from django.contrib.auth.views import LogoutView  # این خط را اضافه کنید
from .views import (
    home_view,
    dashboard_view,
    register_view,
    login_view,
    logout_view,
    profile_view,
    account_list_view,  # این ویو جدید را اضافه کنید
    add_account_view,  # این خط را اضافه کنید
    delete_account_view,
)
app_name = 'accounts'

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),  # این خط را اضافه کنید
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # این خط را اضافه کنید    
    path('profile/', profile_view, name='profile'),
    path('accounts/', account_list_view, name='account_list'),  # این خط را اضافه کنید
    path('accounts/add/', add_account_view, name='add_account'),  # این خط را اضافه کنید
path('accounts/delete/<int:account_id>/', delete_account_view, name='delete_account'),

]