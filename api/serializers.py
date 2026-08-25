"""
Serializers convert Model instances ↔ JSON.

When a client sends JSON → serializer validates it and creates/updates a Note.
When we return a Note → serializer turns it into JSON for the response.
"""

from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    ModelSerializer auto-builds fields from the Note model.
    We only list which fields to include in the API.
    """

    class Meta:
        model = Note
        fields = ['id', 'title', 'body', 'created_at']
        # id and created_at are read-only by default (set by the database)
