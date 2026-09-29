from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Topic, Profile, Contact
from .forms import ContactForm, TopicManageForm


# ---------------------------------------------------------------------------
# Contact saves — KEEP SEPARATE (do not mix)
#   LearnHub  → Contact messages only
#   Portfolio → Profile only
# ---------------------------------------------------------------------------

def _save_learnhub_contact(form):
    """LearnHub form → Contact table only (Admin → Contact messages)."""
    name = form.cleaned_data["name"].strip()
    email = form.cleaned_data["email"].strip().lower()
    message = form.cleaned_data["message"]

    Contact.objects.create(
        name=name,
        email=email,
        message=message,
        profile=None,
    )


def _save_portfolio_contact(request, form):
    """Portfolio form → Profile table only (Admin → Profiles)."""
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


def _portfolio(request, section="home", extra=None):
    ctx = {"section": section}
    if extra:
        ctx.update(extra)
    return render(request, "portfolio/shell.html", ctx)


# ---------------------------------------------------------------------------
# LearnHub  →  templates/learnhub/
# ---------------------------------------------------------------------------

def home(request):
    return render(request, "learnhub/home.html")


def about(request):
    return render(request, "learnhub/about.html")


def topics(request):
    all_topics = Topic.objects.all()
    form = TopicManageForm()
    return render(
        request,
        "learnhub/topics.html",
        {"topics": all_topics, "topic_form": form},
    )


def topic_manage(request):
    """POST from Topics modal: add topic; optionally delete one; or delete only."""
    if request.method != "POST":
        return redirect("topics")

    action = request.POST.get("action", "add")

    if action == "delete":
        pk = request.POST.get("remove_topic")
        if pk:
            topic = Topic.objects.filter(pk=pk).first()
            if topic:
                title = topic.title
                topic.delete()
                messages.success(request, f'Removed topic "{title}".')
        return redirect("topics")

    # action == add (default)
    form = TopicManageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"].strip()
        tag = form.cleaned_data["tag"].strip()
        summary = form.cleaned_data["summary"].strip()
        body = (form.cleaned_data.get("body") or "").strip() or summary
        resource_url = form.cleaned_data.get("resource_url") or ""
        resource_label = (form.cleaned_data.get("resource_label") or "").strip() or "Learn more"
        remove = form.cleaned_data.get("remove_topic")

        Topic.objects.create(
            title=title,
            tag=tag,
            summary=summary,
            body=body,
            resource_url=resource_url,
            resource_label=resource_label,
        )

        if remove:
            removed_title = remove.title
            remove.delete()
            messages.success(
                request,
                f'Added "{title}" and removed "{removed_title}".',
            )
        else:
            messages.success(request, f'Added topic "{title}".')
    else:
        messages.error(request, "Could not save topic. Check the form fields (link must be a valid URL if provided).")

    return redirect("topics")


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, "learnhub/topic_detail.html", {"topic": topic})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            _save_learnhub_contact(form)
            return redirect("contact_success")
    else:
        form = ContactForm()
    return render(request, "learnhub/contact.html", {"form": form})


def contact_success(request):
    return render(request, "learnhub/contact_success.html")


# ---------------------------------------------------------------------------
# Portfolio  →  templates/portfolio/
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
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            _save_portfolio_contact(request, form)
            return redirect("portfolio_contact_success")
    else:
        form = ContactForm()
    return _portfolio(request, "contact", {"form": form})


def portfolio_contact_success(request):
    return _portfolio(request, "contact_success")
