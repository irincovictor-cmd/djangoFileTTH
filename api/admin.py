from django.contrib import admin
from .models import Topic, Contact, Profile


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "resource_url", "created_at")
    search_fields = ("title", "tag", "summary")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    One row per person (email + name).
    Does NOT list full messages here — open Contacts for the inbox.
    """

    list_display = (
        "name",
        "email",
        "contact_count",
        "last_contact_at",
        "user",
        "created_at",
    )
    search_fields = ("name", "email", "notes")
    list_filter = ("last_contact_at",)
    readonly_fields = (
        "contact_count",
        "last_contact_at",
        "last_message",
        "created_at",
        "updated_at",
    )
    # No ContactInline — messages live only under Contacts admin
    fieldsets = (
        (
            "Person",
            {
                "fields": ("name", "email", "user", "notes"),
                "description": (
                    "Identity only. Each unique email + name is one Profile. "
                    "To read messages, use Admin → Contacts."
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


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Message inbox — one row per form submission.
    This is where you read what people wrote.
    """

    list_display = (
        "created_at",
        "name",
        "email",
        "message_preview",
        "profile_link",
    )
    list_display_links = ("created_at", "message_preview")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    readonly_fields = ("name", "email", "message", "profile", "created_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        (
            "Message",
            {
                "fields": ("name", "email", "message", "created_at"),
                "description": "Single contact-form submission (LearnHub or Portfolio).",
            },
        ),
        (
            "Linked profile",
            {
                "fields": ("profile",),
                "description": "Person record (email + name). Edit profile notes there if needed.",
            },
        ),
    )

    @admin.display(description="Message")
    def message_preview(self, obj):
        text = (obj.message or "").strip()
        if not text:
            return "—"
        return text[:80] + ("…" if len(text) > 80 else "")

    @admin.display(description="Profile")
    def profile_link(self, obj):
        if not obj.profile_id:
            return "—"
        return str(obj.profile)

    def has_add_permission(self, request):
        # Messages come from the public forms only
        return False
