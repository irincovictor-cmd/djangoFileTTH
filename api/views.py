"""
Views handle HTTP requests and return responses.

ModelViewSet is a shortcut that gives you full CRUD automatically:
  GET    /api/notes/       → list all notes
  POST   /api/notes/       → create a note
  GET    /api/notes/1/     → retrieve one note
  PUT    /api/notes/1/     → update a note
  PATCH  /api/notes/1/     → partial update
  DELETE /api/notes/1/     → delete a note
"""

from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    # Which rows to work with (newest first)
    queryset = Note.objects.all().order_by('-created_at')

    # How to convert between Note and JSON
    serializer_class = NoteSerializer
