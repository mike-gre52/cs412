#file: restaurant/urls.py

# Created by Mike Greene

# file for defining urls within the restaurant app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    path(r'', views.main, name="main"),
    path(r'main', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'submit', views.submit, name="submit"),
]
