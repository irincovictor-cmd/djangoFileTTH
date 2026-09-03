from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home_page'),

    path('topics/', views.topics, name='topics'),
    path('topics/<int:pk>/', views.topic_detail, name='topic_detail'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
