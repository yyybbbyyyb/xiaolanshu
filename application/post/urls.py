from django.urls import path

from api import *
# Create your views here.

urlpatterns = [
    path('detail', get_detail, name='get_detail'),
    path('recommend', get_recommend, name='get_recommend'),

]