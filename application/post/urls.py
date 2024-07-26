from django.urls import path

from .api import *
# Create your views here.

urlpatterns = [
    path('detail', get_detail, name='get_detail'),
    path('recommend', get_recommend, name='get_recommend'),
    path('upload/info', upload_info, name='upload_info'),
    path('upload/images', upload_image, name='upload_image'),
    path('delete', delete_post, name='delete_post'),


    path('main', comment_main, name='comment_main'),
    path('reply', comment_reply, name='comment_reply'),
    path('get-main', get_main_comments, name='get_main_comments'),
    path('get-reply', get_reply_comments, name='get_reply_comments'),
]