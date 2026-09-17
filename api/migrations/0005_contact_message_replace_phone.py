from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_contact"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contact",
            name="contact",
        ),
        migrations.AddField(
            model_name="contact",
            name="message",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
