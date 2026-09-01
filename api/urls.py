from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home_alt'),  # also support /home/
    path('about/', views.about, name='about'),
]
