from django.db import models


class Department(models.Model):
    """Company department — code, name, head, office location, date established."""

    code = models.CharField(max_length=50, unique=True, help_text="Department code, e.g. DP20261001")
    name = models.CharField(max_length=200, help_text="Department name")
    head = models.CharField(max_length=150, help_text="Department head / manager")
    office_location = models.CharField(max_length=200, help_text="Office location")
    date_established = models.DateField(help_text="Date the department was established")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_established", "name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return f"{self.code} — {self.name}"
