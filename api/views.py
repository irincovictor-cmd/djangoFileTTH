from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Topic, Profile, Contact
from .forms import ContactForm


def home(request):
    """LearnHub home."""
    return render(request, "home.html")


def portfolio(request):
    """Alias for home (legacy URL)."""
    return render(request, "home.html")


def work(request):
    return render(request, "home.html")


def skills(request):
    return render(request, "home.html")


def about(request):
    """LearnHub about page."""
    return render(request, "about.html")


def topics(request):
    all_topics = Topic.objects.all()
    return render(request, "topics.html", {"topics": all_topics})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "topic_detail.html", {"topic": topic})


def contact(request):
    """
    LearnHub contact form → Profile + Contact rows.
    Same email + same name updates Profile; different name = new Profile.
    Each submit also creates a Contact row (admin list + Profile inline).
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
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

            return redirect("contact_success")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def contact_success(request):
    """LearnHub success page after contact submit."""
    return render(request, "contact_success.html")
