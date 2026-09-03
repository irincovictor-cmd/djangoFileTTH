from django.shortcuts import render, get_object_or_404
from .models import Topic


def home(request):
    """Home page with hero and CTA buttons."""
    return render(request, 'home.html')


def topics(request):
    """
    Topics list — loaded from the database (Topic model).
    Not hard-coded HTML cards anymore.
    """
    all_topics = Topic.objects.all()
    return render(request, 'topics.html', {
        'topics': all_topics,
    })


def topic_detail(request, pk):
    """
    Single topic page.
    pk = the topic's id from the URL, e.g. /topics/3/
    """
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, 'topic_detail.html', {
        'topic': topic,
    })


def about(request):
    """About us page."""
    return render(request, 'about.html')


def contact(request):
    """
    Contact page.
    GET  → show the form
    POST → show a simple success message (no real email yet)
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        return render(request, 'contact.html', {
            'success': True,
            'name': name,
        })
    return render(request, 'contact.html')
