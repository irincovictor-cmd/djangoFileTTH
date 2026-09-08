from django.contrib import admin
from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'resource_url', 'created_at')
    search_fields = ('title', 'tag', 'summary')
    fields = ('title', 'tag', 'summary', 'body', 'resource_url', 'resource_label')
