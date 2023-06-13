from . import views
from django.urls import path
urlpatterns = [
    path('', views.home, name='home'),
    # Diğer URL desenleri buraya eklenebilir
]