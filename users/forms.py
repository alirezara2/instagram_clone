from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile

class RegisterForm(UserCreationForm):
    """فرم ثبت‌نام با ایمیل"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})
    )

    class Meta:
        model = CustomUser
        fields = ('email',)

class LoginForm(AuthenticationForm):
    """فرم لاگین با ایمیل"""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'})
    )

class ProfileEditForm(forms.ModelForm):
    """فرم ویرایش پروفایل"""
    class Meta:
        model = Profile
        fields = ('full_name', 'bio', 'birth_date', 'phone_number', 'profile_picture')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'درباره من...'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تماس'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class SearchForm(forms.Form):
    """فرم جستجو"""
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'جستجو...'})
    )