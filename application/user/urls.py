from django.urls import path

from .api import *


urlpatterns = [
    path('register', user_register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('delete', user_delete, name='delete'),
    path('change_avatar', user_change_avatar, name='change_avatar'),
    path('change_password', user_change_password, name='change_password'),


    path('refresh_token', refresh_token, name='refresh_token'),
]