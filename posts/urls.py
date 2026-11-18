from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('explore/', views.explore_view, name='explore'),
    path('post/create/', views.post_create_view, name='post_create'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/delete/', views.post_delete_view, name='post_delete'),
    path('post/<int:post_id>/comment/', views.add_comment_view, name='add_comment'),
    path('post/<int:post_id>/like/', views.like_toggle_view, name='like_toggle'),
]