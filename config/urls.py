"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('departments/', include('department_management.urls')),
    path('', include('api.urls')),  # LearnHub + Portfolio
]
