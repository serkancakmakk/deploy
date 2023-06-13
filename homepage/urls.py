from django import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.static import static
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
urlpatterns = [
path('', views.home, name='home'),
path('<int:year>/<str:month>/', views.home, name='home'),
path('mekan_ekle/', views.mekanekle, name='mekanekle'),
]