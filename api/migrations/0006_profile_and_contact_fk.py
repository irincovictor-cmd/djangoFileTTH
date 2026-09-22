from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_contact_message_replace_phone"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "contact_count",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="How many times this person submitted the contact form",
                    ),
                ),
                ("last_contact_at", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, help_text="Admin notes about this person")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        help_text="Optional link if they also have a Django login",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Profile",
                "verbose_name_plural": "Profiles",
                "ordering": ["-last_contact_at", "-created_at"],
            },
        ),
        migrations.AddField(
            model_name="contact",
            name="profile",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contacts",
                to="api.profile",
            ),
        ),
    ]
