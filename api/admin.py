from django.contrib import admin
from .models import Topic, Contact, Profile


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "resource_url", "created_at")
    search_fields = ("title", "tag", "summary")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Portfolio contacts only — one row per person (email + name).
    LearnHub messages are under Contact messages, not here.
    """

    list_display = (
        "name",
        "email",
        "contact_count",
        "last_message_preview",
        "last_contact_at",
        "created_at",
    )
    search_fields = ("name", "email", "notes", "last_message")
    list_filter = ("last_contact_at",)
    readonly_fields = (
        "contact_count",
        "last_contact_at",
        "last_message",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Portfolio person",
            {
                "fields": ("name", "email", "user", "notes"),
                "description": (
                    "Data from the Portfolio contact form only. "
                    "LearnHub submissions appear under Contact messages."
                ),
            },
        ),
        (
            "Activity (auto-updated)",
            {
                "fields": (
                    "contact_count",
                    "last_contact_at",
                    "last_message",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.display(description="Last message")
    def last_message_preview(self, obj):
        text = (obj.last_message or "").strip()
        if not text:
            return "—"
        return text[:60] + ("…" if len(text) > 60 else "")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    LearnHub message inbox — one row per form submission.
    Portfolio form does not write here.
    """

    list_display = (
        "created_at",
        "name",
        "email",
        "message_preview",
    )
    list_display_links = ("created_at", "message_preview")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    readonly_fields = ("name", "email", "message", "profile", "created_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    exclude = ("profile",)  # hide linked profile — LearnHub no longer sets it

    fieldsets = (
        (
            "LearnHub message",
            {
                "fields": ("name", "email", "message", "created_at"),
                "description": "Submission from LearnHub /contact/ only.",
            },
        ),
    )

    @admin.display(description="Message")
    def message_preview(self, obj):
        text = (obj.message or "").strip()
        if not text:
            return "—"
        return text[:80] + ("…" if len(text) > 80 else "")

    def has_add_permission(self, request):
        return False
