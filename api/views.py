from django.shortcuts import render, get_object_or_404, redirect
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
    POST → validate, save to DB, redirect to success page
    (Matches the course pattern: redirect("contact_success"))
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # store in database (extra vs bare sample)
            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def contact_success(request):
    """Shown after a successful contact form submit."""
    return render(request, 'contact_success.html')
