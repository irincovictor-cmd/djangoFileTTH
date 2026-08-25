"""
Main URL configuration for the whole project.

When a request comes in (e.g. /api/notes/), Django looks here first,
then follows include() into the app's urls.py.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin dashboard → http://localhost:8081/admin/
    path('admin/', admin.site.urls),

    # All API routes live under /api/
    # Example: /api/notes/ is handled inside api/urls.py
    path('api/', include('api.urls')),
]
