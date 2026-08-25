"""
Models = database tables.

Each class that inherits from models.Model becomes a table.
Each field becomes a column.

After changing models, always run:
  python manage.py makemigrations
  python manage.py migrate
"""

from django.db import models


class Note(models.Model):
    """A simple note with a title and body."""

    # Short text (max 200 characters) — becomes VARCHAR in the database
    title = models.CharField(max_length=200)

    # Longer text — becomes TEXT in the database
    body = models.TextField()

    # Auto-set when the row is first created (never updated after that)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # How this object appears in the admin and in print()
        return self.title
