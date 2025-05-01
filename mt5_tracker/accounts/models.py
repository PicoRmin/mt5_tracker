import secrets
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    
    # فیلدهای اضافه شده
    phone = models.CharField(
        _('شماره تلفن'),
        max_length=15,
        blank=True,
        null=True,
        unique=True
    )
    
    api_token = models.CharField(
        _('توکن API'),
        max_length=64,
        blank=True,
        null=True,
        unique=True
    )
    
    is_trader = models.BooleanField(
        _('معامله گر؟'),
        default=False
    )
    
    broker_name = models.CharField(
        _('نام بروکر'),
        max_length=100,
        blank=True,
        null=True
    )
    
    # تنظیمات متا
    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')
        ordering = ['-date_joined']
        
        
    api_token = models.CharField(max_length=64, unique=True, blank=True, null=True)
    # متدهای سفارشی
    def generate_api_token(self):
        """تولید توکن تصادفی 32 بایتی"""
        if not self.api_token:
            self.api_token = secrets.token_hex(32)
            self.save()
        return self.api_token

    def save(self, *args, **kwargs):
        """تولید خودکار توکن هنگام ایجاد کاربر جدید"""
        if not self.pk or not self.api_token:
            self.generate_api_token()
        super().save(*args, **kwargs)
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def __str__(self):
        return self.username

# Signal برای ایجاد توکن API هنگام ساخت کاربر جدید
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.api_token:
        instance.generate_api_token()