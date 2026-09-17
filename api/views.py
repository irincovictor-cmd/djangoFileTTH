from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic
from .forms import ContactForm


def home(request):
    """Home — prefers portfolio template if present."""
    return render(request, "portfolio.html")


def portfolio(request):
    """Explicit portfolio route (Laravel-style sections can live in one HTML)."""
    return render(request, "portfolio.html")


def topics(request):
    all_topics = Topic.objects.all()
    return render(request, "topics.html", {"topics": all_topics})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "topic_detail.html", {"topic": topic})


def about(request):
    return render(request, "about.html")


def contact(request):
    """
    Contact form: name, email, message.
    POST → validate → save to DB → redirect success.
    Manage rows in /admin/ → Contacts.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact_success")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def contact_success(request):
    return render(request, "contact_success.html")
