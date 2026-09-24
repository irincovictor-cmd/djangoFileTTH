from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Topic, Profile, Contact
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


def skills(request):
    return _portfolio(request, "skills")


def about(request):
    return _portfolio(request, "about")


def topics(request):
    all_topics = Topic.objects.all()
    return render(request, "topics.html", {"topics": all_topics})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "topic_detail.html", {"topic": topic})


def contact(request):
    """
    Portfolio contact → Profile (admin source of truth).
    Same email = same Profile; last_message + count updated each submit.
    Message history is also stored as Contact rows (inline under Profile only).
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"].strip().lower()
            message = form.cleaned_data["message"]

            profile, _created = Profile.objects.get_or_create(
                email=email,
                defaults={"name": name, "last_message": message},
            )
            if profile.name != name:
                profile.name = name

            # Link Django user only if free (OneToOne)
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

            # History row (visible only as Profile inline in admin)
            Contact.objects.create(
                profile=profile,
                name=name,
                email=email,
                message=message,
            )

            return redirect("contact_success")
    else:
        form = ContactForm()

    return _portfolio(request, "contact", {"form": form})


def contact_success(request):
    return _portfolio(request, "contact_success")
