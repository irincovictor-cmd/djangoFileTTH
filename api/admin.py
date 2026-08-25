"""
Register models here so they appear in the Django admin at /admin/.
"""

from django.contrib import admin
from .models import Note

# Simple registration — you can customize the admin later
admin.site.register(Note)
