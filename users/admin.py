from django.contrib import admin
from .models import CustomUser, Profile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'created_at')
    search_fields = ('user__email', 'full_name')