from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # Root / redirects to /home/ so the address bar shows a clear path
    path('', lambda request: redirect('home'), name='root'),

    # Main pages
    path('home/', views.home, name='home'),
    path('topics/', views.topics, name='topics'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
