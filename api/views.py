from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Topic, Profile, Contact
from .forms import ContactForm, TopicManageForm, TopicEditForm


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


def _get_active_topic_or_fallback(request, pk):
    """Return active topic, or redirect to topics with a clear message.

    Covers: deleted in Admin, purged from bin, or sitting in recycle bin.
    """
    topic = Topic.objects.active().filter(pk=pk).first()
    if topic:
        return topic

    if Topic.objects.deleted().filter(pk=pk).exists():
        messages.warning(
            request,
            "That topic is in the recycle bin. Restore it from Topics → Recycle bin if you still need it.",
        )
    else:
        messages.warning(
            request,
            "That topic is no longer available. It may have been deleted. Browse the list below.",
        )
    return None


# ---------------------------------------------------------------------------
# LearnHub  →  templates/learnhub/
# ---------------------------------------------------------------------------

def home(request):
    return render(request, "learnhub/home.html")


def about(request):
    return render(request, "learnhub/about.html")


def topics(request):
    all_topics = Topic.objects.active()
    deleted_topics = Topic.objects.deleted().order_by("-deleted_at")
    form = TopicManageForm()
    return render(
        request,
        "learnhub/topics.html",
        {
            "topics": all_topics,
            "deleted_topics": deleted_topics,
            "topic_form": form,
        },
    )


def topic_manage(request):
    """POST: add topic, soft-delete (from edit page), restore, or permanent delete."""
    if request.method != "POST":
        return redirect("topics")

    action = request.POST.get("action", "add")

    # ---- Soft-delete (from Edit topic page) ----
    if action == "delete":
        pk = request.POST.get("topic_id") or request.POST.get("remove_topic")
        if not pk:
            messages.error(request, "No topic selected to move to the recycle bin.")
            return redirect("topics")
        topic = Topic.objects.active().filter(pk=pk).first()
        if topic:
            title = topic.title
            topic.soft_delete()
            messages.success(request, f'Moved "{title}" to the recycle bin.')
        else:
            messages.error(request, "That topic was not found (or is already in the bin).")
        return redirect("topics")

    # ---- Restore from bin ----
    if action == "restore":
        pk = request.POST.get("bin_topic")
        topic = Topic.objects.deleted().filter(pk=pk).first() if pk else None
        if topic:
            title = topic.title
            topic.restore()
            messages.success(request, f'Restored "{title}" from the recycle bin.')
        else:
            messages.error(request, "Could not restore that topic.")
        return redirect("topics")

    # ---- Permanent delete from bin ----
    if action == "purge":
        pk = request.POST.get("bin_topic")
        topic = Topic.objects.deleted().filter(pk=pk).first() if pk else None
        if topic:
            title = topic.title
            topic.delete()
            messages.success(request, f'Permanently deleted "{title}".')
        else:
            messages.error(request, "Could not permanently delete that topic.")
        return redirect("topics")

    # ---- Add only ----
    form = TopicManageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"].strip()
        tag = form.cleaned_data["tag"].strip()
        summary = form.cleaned_data["summary"].strip()
        body = (form.cleaned_data.get("body") or "").strip() or summary
        resource_url = form.cleaned_data.get("resource_url") or ""
        resource_label = (form.cleaned_data.get("resource_label") or "").strip() or "Learn more"

        Topic.objects.create(
            title=title,
            tag=tag,
            summary=summary,
            body=body,
            resource_url=resource_url,
            resource_label=resource_label,
        )
        messages.success(request, f'Added topic "{title}".')
    else:
        messages.error(
            request,
            "Could not save topic. Check the form fields (link must be a valid URL if provided).",
        )

    return redirect("topics")


def topic_edit(request, pk):
    """Edit an active topic; soft-delete is available on this page (not on Add)."""
    topic = _get_active_topic_or_fallback(request, pk)
    if topic is None:
        return redirect("topics")

    if request.method == "POST":
        form = TopicEditForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated topic "{topic.title}".')
            return redirect("topic_detail", pk=topic.pk)
    else:
        form = TopicEditForm(instance=topic)

    return render(
        request,
        "learnhub/topic_edit.html",
        {"form": form, "topic": topic},
    )


def topic_detail(request, pk):
    topic = _get_active_topic_or_fallback(request, pk)
    if topic is None:
        return redirect("topics")
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
