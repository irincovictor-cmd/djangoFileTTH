from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_profile_last_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="email",
            field=models.EmailField(
                help_text="Not unique alone — same email + different name = different profiles",
                max_length=254,
            ),
        ),
        migrations.AddConstraint(
            model_name="profile",
            constraint=models.UniqueConstraint(
                fields=("email", "name"),
                name="unique_profile_email_name",
            ),
        ),
    ]
