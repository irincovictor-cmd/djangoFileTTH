from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_topic_deleted_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="TopicHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("added", "Added"),
                            ("deleted", "Moved to recycle bin"),
                            ("restored", "Restored"),
                            ("purged", "Permanently deleted"),
                            ("updated", "Updated"),
                        ],
                        max_length=20,
                    ),
                ),
                ("topic_title", models.CharField(help_text="Title at the time of the event", max_length=200)),
                ("topic_tag", models.CharField(blank=True, max_length=50)),
                (
                    "topic_id",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Topic pk when still known (null after permanent delete)",
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Topic history",
                "verbose_name_plural": "Topic history",
                "ordering": ["-created_at"],
            },
        ),
    ]
