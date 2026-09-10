from django.contrib import admin
from .models import Topic, Contact


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'resource_url', 'created_at')
    search_fields = ('title', 'tag', 'summary')
    fields = ('title', 'tag', 'summary', 'body', 'resource_url', 'resource_label')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact', 'created_at')
    search_fields = ('name', 'email', 'contact')
    readonly_fields = ('created_at',)
