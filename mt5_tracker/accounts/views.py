import secrets
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from trading.models import MT5Account
from .forms import CustomUserCreationForm  # این خط را اضافه کنید
from .models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Create your views here.
from django.contrib.auth.decorators import login_required

def home_view(request):
    # اگر کاربر لاگین کرده باشد به داشبورد هدایت شود
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # صفحه اصلی برای کاربران مهمان
    return render(request, 'home.html', {})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # استفاده از فرم سفارشی
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = CustomUserCreationForm()  # استفاده از فرم سفارشی
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def account_list_view(request):
    accounts = MT5Account.objects.filter(user=request.user)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})    

@login_required
def add_account_view(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        broker = request.POST.get('broker')
        
        # ایجاد حساب جدید
        MT5Account.objects.create(
            user=request.user,
            account_id=account_id,
            broker=broker,
            token=secrets.token_hex(16)  # تولید توکن تصادفی
        )
        return redirect('accounts:account_list')
    
    return redirect('accounts:account_list')

@login_required
def delete_account_view(request, account_id):
    # دریافت حساب یا نمایش خطای 404 اگر وجود نداشته باشد
    account = get_object_or_404(MT5Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        # حذف حساب
        account.delete()
        messages.success(request, 'حساب با موفقیت حذف شد.')
        return redirect('accounts:account_list')
    
    # اگر درخواست POST نبود، کاربر را به لیست حساب‌ها هدایت کن
    return redirect('accounts:account_list')



