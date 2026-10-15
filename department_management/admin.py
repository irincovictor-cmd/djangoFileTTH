from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "head", "office_location", "date_established")
    search_fields = ("code", "name", "head", "office_location")
    list_filter = ("date_established",)
    ordering = ("-date_established",)
