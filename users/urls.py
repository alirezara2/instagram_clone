from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<str:email>/', views.profile_view, name='user_profile'),
    path('search/', views.search_view, name='search'),
    path('follow/<str:email>/', views.follow_toggle_view, name='follow_toggle'),
]