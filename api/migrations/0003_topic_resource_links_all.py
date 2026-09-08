from django.db import migrations


# Each key matches part of Topic.title (case-insensitive).
# URLs are official docs for that exact subject — not random pages.
TOPIC_RESOURCES = [
    {
        'match': 'django',
        'url': 'https://docs.djangoproject.com/en/stable/intro/overview/',
        'label': 'Official Django docs — overview',
    },
    {
        'match': 'urls',
        'url': 'https://docs.djangoproject.com/en/stable/topics/http/urls/',
        'label': 'Django docs — URL dispatcher',
    },
    {
        'match': 'html',
        'url': 'https://docs.djangoproject.com/en/stable/topics/templates/',
        'label': 'Django docs — templates',
    },
    {
        'match': 'user input',
        'url': 'https://docs.djangoproject.com/en/stable/topics/forms/',
        'label': 'Django docs — forms',
    },
    {
        'match': 'models',
        'url': 'https://docs.djangoproject.com/en/stable/topics/migrations/',
        'label': 'Django docs — migrations',
    },
    {
        'match': 'save your work',
        'url': 'https://git-scm.com/doc',
        'label': 'Official Git documentation',
    },
]


def set_all_resources(apps, schema_editor):
    Topic = apps.get_model('api', 'Topic')
    for item in TOPIC_RESOURCES:
        topic = Topic.objects.filter(title__icontains=item['match']).order_by('id').first()
        if topic is not None:
            topic.resource_url = item['url']
            topic.resource_label = item['label']
            topic.save()


def clear_resources(apps, schema_editor):
    """Reverse: only clear URLs we set (optional rollback)."""
    Topic = apps.get_model('api', 'Topic')
    urls = {item['url'] for item in TOPIC_RESOURCES}
    for topic in Topic.objects.all():
        if topic.resource_url in urls:
            topic.resource_url = ''
            topic.resource_label = 'Learn more'
            topic.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_topic_resource_link'),
    ]

    operations = [
        migrations.RunPython(set_all_resources, clear_resources),
    ]
