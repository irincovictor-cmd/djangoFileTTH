from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic
from .forms import ContactForm


def _portfolio(request, section="home", extra=None):
    """Portfolio pages share one template + nav."""
    ctx = {"section": section}
    if extra:
        ctx.update(extra)
    return render(request, "portfolio.html", ctx)


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
    """Portfolio contact section — still saves name/email/message to DB."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact_success")
    else:
        form = ContactForm()

    return _portfolio(request, "contact", {"form": form})


def contact_success(request):
    return _portfolio(request, "contact_success")
