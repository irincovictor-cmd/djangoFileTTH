from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_profile_email_name_unique"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="deleted_at",
            field=models.DateTimeField(
                blank=True,
                help_text="When set, topic is in the recycle bin (not shown on /topics/).",
                null=True,
            ),
        ),
    ]
