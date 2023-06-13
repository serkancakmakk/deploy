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
path('get-ilceler/<int:sehir_id>/', views.get_ilceler, name='get_ilceler'),  
path('update_profile', views.update_profile, name='update_profile'),
path('register/', views.register, name='register'),
path('login/', views.login_view, name='login'),
path('my_profile/', views.my_profile, name='my_profile'),
]