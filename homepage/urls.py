from . import views
from django.urls import path
path('', views.home, name='home'),