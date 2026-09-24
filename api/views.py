from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Topic, Profile, Contact
from .forms import ContactForm


# ---------------------------------------------------------------------------
# Shared contact save (used by LearnHub + Portfolio forms)
# ---------------------------------------------------------------------------

def _save_contact_submission(request, form):
    """
    Persist a valid ContactForm: Profile (email+name) + Contact history row.
    Returns True on success.
    """
    name = form.cleaned_data["name"].strip()
    email = form.cleaned_data["email"].strip().lower()
    message = form.cleaned_data["message"]

    profile, _created = Profile.objects.get_or_create(
        email=email,
        name=name,
        defaults={"last_message": message},
    )

    if (
        request.user.is_authenticated
        and profile.user_id is None
        and not Profile.objects.filter(user=request.user).exists()
    ):
        profile.user = request.user

    profile.last_message = message
    profile.contact_count = (profile.contact_count or 0) + 1
    profile.last_contact_at = timezone.now()
    profile.save()

    Contact.objects.create(
        profile=profile,
        name=name,
        email=email,
        message=message,
    )
    return True


def _portfolio(request, section="home", extra=None):
    """Render dark portfolio shell with a section flag."""
    ctx = {"section": section}
    if extra:
        ctx.update(extra)
    return render(request, "portfolio.html", ctx)


# ---------------------------------------------------------------------------
# LearnHub
# ---------------------------------------------------------------------------

def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def topics(request):
    all_topics = Topic.objects.all()
    return render(request, "topics.html", {"topics": all_topics})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "topic_detail.html", {"topic": topic})


def contact(request):
    """LearnHub contact — notebook UI, saves to same DB as portfolio."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            _save_contact_submission(request, form)
            return redirect("contact_success")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


def contact_success(request):
    return render(request, "contact_success.html")


# ---------------------------------------------------------------------------
# Portfolio (separate URLs + template — no clash with LearnHub)
# ---------------------------------------------------------------------------

def portfolio_home(request):
    return _portfolio(request, "home")


def portfolio_work(request):
    return _portfolio(request, "work")


def portfolio_skills(request):
    return _portfolio(request, "skills")


def portfolio_about(request):
    return _portfolio(request, "about")


def portfolio_contact(request):
    """Portfolio contact — dark UI; same Profile/Contact save as LearnHub."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            _save_contact_submission(request, form)
            return redirect("portfolio_contact_success")
    else:
        form = ContactForm()
    return _portfolio(request, "contact", {"form": form})


def portfolio_contact_success(request):
    return _portfolio(request, "contact_success")
