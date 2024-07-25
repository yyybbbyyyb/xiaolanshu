from django.urls import path

from .api import *


urlpatterns = [
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('delete/', user_delete, name='delete'),
    path('change-avatar', user_change_avatar, name='change_avatar'),
    path('change-password', user_change_password, name='change_password'),
    path('change-info', user_change_info, name='change_info'),
    path('get-info', user_get_info, name='get_info'),
    path('get-info-by-id', user_get_info_by_id, name='get_info_by_id'),

    path('refresh-token', refresh_token, name='refresh_token'),

    path('get-user-action-info', get_user_action_info, name='get_user_action_info'),
]