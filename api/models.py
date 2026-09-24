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
    Contact identity keyed by (email + name).
    Same email with a different name → separate Profile so you can backtrack
    who submitted under which name. Same email + same name → one Profile,
    updated on each submit (count + last message).
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
        help_text="Most recent message from the contact form",
    )
    contact_count = models.PositiveIntegerField(
        default=0,
        help_text="How many times this name+email submitted the contact form",
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
        return f"{self.name} <{self.email}> ({self.contact_count} messages)"


class Contact(models.Model):
    """
    Individual contact-form submission (message history).
    Not shown as its own admin page — only as an inline under Profile.
    """

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="contacts",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.email})"
