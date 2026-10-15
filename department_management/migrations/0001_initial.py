from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(help_text="Department code, e.g. DP20261001", max_length=50, unique=True)),
                ("name", models.CharField(help_text="Department name", max_length=200)),
                ("head", models.CharField(help_text="Department head / manager", max_length=150)),
                ("office_location", models.CharField(help_text="Office location", max_length=200)),
                ("date_established", models.DateField(help_text="Date the department was established")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Department",
                "verbose_name_plural": "Departments",
                "ordering": ["-date_established", "name"],
            },
        ),
    ]
