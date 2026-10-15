from django.db import models
from department_management.models import Department


class Employee(models.Model):
    """Employee — managed in Django Admin only (no public web pages)."""

    employee_id = models.CharField(max_length=50, unique=True, help_text="Employee ID / code")
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    position = models.CharField(max_length=150, help_text="Job title / position")
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
    )
    hire_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"{self.employee_id} — {self.name}"
