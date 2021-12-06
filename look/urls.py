from django.urls import path, register_converter
from . import views
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from . views import *


urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('like/', views.like_post, name='like_post'),
    path('dislike/', views.dislike_post, name='dislike_post'),
]