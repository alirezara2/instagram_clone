from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """مدیر مدل کاربر سفارشی برای لاگین با ایمیل"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('ایمیل الزامی است')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser باید is_staff=True باشد')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser باید is_superuser=True باشد')
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """مدل کاربر سفارشی با ایمیل به عنوان فیلد اصلی"""
    
    username = None
    email = models.EmailField('ایمیل', unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()  # type: ignore
    
    def __str__(self):
        return self.email


class Profile(models.Model):
    """مدل پروفایل کاربر"""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    full_name = models.CharField('نام و نام خانوادگی', max_length=100, blank=True)
    bio = models.TextField('بیوگرافی', max_length=500, blank=True)
    birth_date = models.DateField('تاریخ تولد', null=True, blank=True)
    phone_number = models.CharField('شماره تماس', max_length=15, blank=True)
    profile_picture = models.ImageField(
        'عکس پروفایل', 
        upload_to='profiles/', 
        blank=True,
        null=True
    )
    created_at = models.DateTimeField('تاریخ ساخت', auto_now_add=True)
    updated_at = models.DateTimeField('آخرین بروزرسانی', auto_now=True)

    def __str__(self):
        return f"پروفایل {self.user.email}"


class Follow(models.Model):
    """مدل دنبال کردن کاربران"""
    
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.email} -> {self.following.email}"