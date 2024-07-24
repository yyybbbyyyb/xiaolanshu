from django.urls import path

from .api import *

urlpatterns = [
    path('get-counters', get_counters, name='get_counters'),

    path('counter/get-dishes', get_dishes, name='get_dishes'),

    path('get-all-cafeterias', get_all_cafeterias, name='get_all_cafeterias'),

]
