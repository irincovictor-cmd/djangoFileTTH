from django.conf import settings
from django.db import models


class Topic(models.Model):
    """Educational topic for LearnHub topics page."""

    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=50, help_text="Short label, e.g. Django, Git")
    summary = models.TextField(help_text="Short description on the topics list")
    body = models.TextField(help_text="Longer explanation on the detail page")
    resource_url = models.URLField(blank=True)
    resource_label = models.CharField(max_length=100, blank=True, default="Learn more")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title


class Profile(models.Model):
    """
    Person who used a contact form (keyed by email + name).
    Activity stats only — full messages are Contact rows (Admin → Contacts).
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile",
        help_text="Optional link if they also have a Django login",
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(
        help_text="Not unique alone — same email + different name = different profiles",
    )
    last_message = models.TextField(
        blank=True,
        help_text="Snapshot of the latest message (read full history in Contacts)",
    )
    contact_count = models.PositiveIntegerField(
        default=0,
        help_text="How many times this name+email submitted a contact form",
    )
    last_contact_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="Admin notes about this person")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_contact_at", "-created_at"]
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        constraints = [
            models.UniqueConstraint(
                fields=["email", "name"],
                name="unique_profile_email_name",
            ),
        ]

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Contact(models.Model):
    """
    One contact-form submission = one message.
    Admin → Contacts is the inbox. Profile is the person, not the message list.
    """

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="contacts",
        null=True,
        blank=True,
        help_text="Person (email + name) this message belongs to",
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact message"
        verbose_name_plural = "Contact messages"

    def __str__(self):
        preview = (self.message or "")[:40]
        return f"{self.name}: {preview}"
