from django.shortcuts import render, get_object_or_404
from .models import Topic
from .forms import ContactForm


def home(request):
    """Home page with hero and CTA buttons."""
    return render(request, 'home.html')


def topics(request):
    """Topics list — loaded from the database."""
    all_topics = Topic.objects.all()
    return render(request, 'topics.html', {
        'topics': all_topics,
    })


def topic_detail(request, pk):
    """Single topic page."""
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, 'topic_detail.html', {
        'topic': topic,
    })


def about(request):
    """About us page."""
    return render(request, 'about.html')


def contact(request):
    """
    Contact page using ContactForm (ModelForm).
    GET  → empty form
    POST → validate, save to DB, show success
    """
    success = False
    saved_name = None

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            entry = form.save()  # writes to Contact table
            success = True
            saved_name = entry.name
            form = ContactForm()  # clear form after success
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form,
        'success': success,
        'name': saved_name,
    })
