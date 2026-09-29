from django.conf import settings
from django.db import models
from django.utils import timezone


class TopicQuerySet(models.QuerySet):
    def active(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)


class TopicManager(models.Manager):
    def get_queryset(self):
        return TopicQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def deleted(self):
        return self.get_queryset().deleted()


class Topic(models.Model):
    """Educational topic for LearnHub topics page.

    Soft-delete: deleted_at set → recycle bin (still in this table).
    Permanent delete removes the row entirely.
    """

    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=50, help_text="Category / short label, e.g. Django, Git")
    summary = models.TextField(help_text="Short description on the topics list")
    body = models.TextField(help_text="Longer explanation on the detail page")
    resource_url = models.URLField(blank=True)
    resource_label = models.CharField(max_length=100, blank=True, default="Learn more")
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When set, topic is in the recycle bin (not shown on /topics/).",
    )

    objects = TopicManager()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        if self.deleted_at:
            return f"{self.title} (in recycle bin)"
        return self.title

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])


class Profile(models.Model):
    """
    Portfolio contact submissions only.
    One row per person (email + name). Keeps last message + count.
    LearnHub messages go to Contact — not here.
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
        help_text="Latest message from the Portfolio contact form",
    )
    contact_count = models.PositiveIntegerField(
        default=0,
        help_text="How many times this name+email submitted the Portfolio form",
    )
    last_contact_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="Admin notes about this person")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_contact_at", "-created_at"]
        verbose_name = "Profile"
        verbose_name_plural = "Profiles (Portfolio)"
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
    LearnHub contact-form submissions only (message inbox).
    Portfolio form does NOT write here — it updates Profile only.
    """

    profile = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name="contacts",
        null=True,
        blank=True,
        help_text="Unused for LearnHub-only flow (kept for old rows)",
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact message"
        verbose_name_plural = "Contact messages (LearnHub)"

    def __str__(self):
        preview = (self.message or "")[:40]
        return f"{self.name}: {preview}"
