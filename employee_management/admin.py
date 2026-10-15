from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "name", "position", "department", "email", "hire_date")
    search_fields = ("employee_id", "name", "email", "position")
    list_filter = ("department", "hire_date")
