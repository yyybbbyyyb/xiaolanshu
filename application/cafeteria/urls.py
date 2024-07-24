from django.urls import path

from .api import *

urlpatterns = [
    path('get-counters', get_counters, name='get_counters'),

    path('counter/get-dishes', get_dishes, name='get_dishes'),

    path('get-all-cafeterias', get_all_cafeterias, name='get_all_cafeterias'),

    path('get-cafeteria', get_cafeteria, name='get_cafeteria'),

    path('get-counter', get_counter, name='get_counter'),

]
