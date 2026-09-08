from django.db import migrations, models


def set_django_resource(apps, schema_editor):
    """First topic (What is Django?) gets an official docs link."""
    Topic = apps.get_model('api', 'Topic')
    topic = Topic.objects.filter(title__icontains='Django').order_by('id').first()
    if topic is None:
        topic = Topic.objects.order_by('id').first()
    if topic is not None:
        topic.resource_url = 'https://docs.djangoproject.com/en/stable/intro/overview/'
        topic.resource_label = 'Official Django docs — overview'
        topic.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='resource_label',
            field=models.CharField(
                blank=True,
                default='Learn more',
                help_text='Button text, e.g. Official Django docs',
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name='topic',
            name='resource_url',
            field=models.URLField(
                blank=True,
                help_text='Link to docs or a video for deeper study (leave blank if none)',
            ),
        ),
        migrations.RunPython(set_django_resource, migrations.RunPython.noop),
    ]
