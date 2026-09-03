from django.db import migrations, models


def seed_topics(apps, schema_editor):
    """Insert starter topics so the page is not empty after migrate."""
    Topic = apps.get_model('api', 'Topic')
    starters = [
        {
            'title': 'What is Django?',
            'tag': 'Basics',
            'summary': 'A Python web framework for building sites and APIs quickly with a clear structure.',
            'body': (
                'Django is a high-level Python web framework that encourages rapid development '
                'and clean design. It gives you routing (URLs), views, templates, models, and an '
                'admin panel out of the box. You focus on your app; Django handles a lot of the '
                'boring infrastructure.'
            ),
        },
        {
            'title': 'URLs & Views',
            'tag': 'Routing',
            'summary': 'Map a path like /topics/ to a Python function that returns a page.',
            'body': (
                'In Django, urls.py connects a path to a view function. When a user visits '
                '/topics/, Django looks up that path and runs the matching view. The view '
                'can load data from the database and pass it to a template.'
            ),
        },
        {
            'title': 'HTML with Django',
            'tag': 'Templates',
            'summary': 'Use base templates, blocks, and the url template tag for reusable layouts.',
            'body': (
                'Templates are HTML files with extra Django tags. base.html holds the navbar and '
                'CSS. Other pages extend it and only fill the content block. That way you write '
                'the layout once and reuse it everywhere.'
            ),
        },
        {
            'title': 'User input',
            'tag': 'Forms',
            'summary': 'Collect data with forms, validate it, and show messages back to the user.',
            'body': (
                'Forms send data with POST. In the view you read request.POST, validate the '
                'fields, then save to the database or show a success message. Always include '
                '{% csrf_token %} in forms for security.'
            ),
        },
        {
            'title': 'Models & migrations',
            'tag': 'Database',
            'summary': 'Define tables in Python and apply them with makemigrations and migrate.',
            'body': (
                'A Model is a Python class that becomes a database table. Each field is a column. '
                'makemigrations creates migration files; migrate applies them to the database. '
                'That is how Topic became a real table for this page.'
            ),
        },
        {
            'title': 'Save your work',
            'tag': 'Git',
            'summary': 'Push to GitHub often so lab PC wipes do not erase your progress.',
            'body': (
                'Git tracks changes to your code. GitHub stores a remote copy. After every '
                'meaningful change: git add, git commit, git push. If a lab PC is wiped, you '
                'clone or pull and continue.'
            ),
        },
    ]
    for item in starters:
        Topic.objects.create(**item)


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('tag', models.CharField(help_text='Short label, e.g. Django, Git', max_length=50)),
                ('summary', models.TextField(help_text='Short description on the topics list')),
                ('body', models.TextField(help_text='Longer explanation on the detail page')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.RunPython(seed_topics, migrations.RunPython.noop),
    ]
