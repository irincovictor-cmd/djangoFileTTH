from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic
from .forms import ContactForm


def _portfolio(request, section="home"):
    """Single portfolio template; section mirrors old Laravel portfolio routes."""
    return render(request, "portfolio.html", {"section": section})


def home(request):
    return _portfolio(request, "home")


def portfolio(request):
    return _portfolio(request, "home")


def work(request):
    return _portfolio(request, "work")


def about(request):
    return _portfolio(request, "about")


def topics(request):
    all_topics = Topic.objects.all()
    return render(request, "topics.html", {"topics": all_topics})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "topic_detail.html", {"topic": topic})


def contact(request):
    """name, email, message → Contact table → Admin."""
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
