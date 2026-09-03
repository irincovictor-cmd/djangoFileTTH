from django.urls import path
from . import views

urlpatterns = [
    # Home at BOTH / and /home/ — no redirect (redirects can drop the :8081 port)
    path('', views.home, name='home'),
    path('home/', views.home, name='home_page'),

    path('topics/', views.topics, name='topics'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
