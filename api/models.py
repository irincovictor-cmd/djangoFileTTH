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


class Contact(models.Model):
    """
    Contact form submission: name, email, message.
    Visible in Django Admin → Contacts.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.email})"
