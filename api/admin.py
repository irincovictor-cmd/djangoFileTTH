from django.contrib import admin
from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'created_at')
    search_fields = ('title', 'tag', 'summary')
