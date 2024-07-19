from django.urls import path

from .api import *


urlpatterns = [
    path('register', user_register, name='register'),
    path('login', user_login, name='login'),
    path('refresh_token', refresh_token, name='refresh_token'),
]