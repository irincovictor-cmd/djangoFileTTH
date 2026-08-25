"""
URL routes for the api app.

DefaultRouter automatically creates the routes for a ViewSet:
  /notes/       and  /notes/<id>/

These are included under /api/ by config/urls.py,
so the full paths become:
  /api/notes/
  /api/notes/1/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet

router = DefaultRouter()
router.register('notes', NoteViewSet)  # registers list + detail routes

urlpatterns = [
    path('', include(router.urls)),
]
