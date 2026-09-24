from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_profile_and_contact_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="last_message",
            field=models.TextField(
                blank=True,
                help_text="Most recent message from the contact form",
            ),
        ),
    ]
