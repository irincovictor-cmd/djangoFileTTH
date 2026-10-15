from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("department_management", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_id", models.CharField(help_text="Employee ID / code", max_length=50, unique=True)),
                ("name", models.CharField(max_length=150)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("position", models.CharField(help_text="Job title / position", max_length=150)),
                ("hire_date", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "department",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="employees",
                        to="department_management.department",
                    ),
                ),
            ],
            options={
                "verbose_name": "Employee",
                "verbose_name_plural": "Employees",
                "ordering": ["name"],
            },
        ),
    ]
