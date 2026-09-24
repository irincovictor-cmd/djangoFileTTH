from django.contrib import admin
from .models import Topic, Contact, Profile


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "resource_url", "created_at")
    search_fields = ("title", "tag", "summary")


class ContactInline(admin.TabularInline):
    """Message history under a Profile (no separate Contacts admin page)."""

    model = Contact
    extra = 0
    readonly_fields = ("name", "email", "message", "created_at")
    can_delete = True
    show_change_link = False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "message_preview",
        "contact_count",
        "last_contact_at",
        "user",
        "created_at",
    )
    search_fields = ("name", "email", "notes", "last_message")
    list_filter = ("email", "last_contact_at")
    readonly_fields = (
        "last_message",
        "contact_count",
        "last_contact_at",
        "created_at",
        "updated_at",
    )
    inlines = [ContactInline]
    fieldsets = (
        (None, {"fields": ("name", "email", "user", "notes")}),
        (
            "Contact form data",
            {
                "fields": (
                    "last_message",
                    "contact_count",
                    "last_contact_at",
                    "created_at",
                    "updated_at",
                ),
                "description": (
                    "Profiles are unique by email + name. Same email with a "
                    "different name creates a new Profile so you can backtrack. "
                    "Full message history is below."
                ),
            },
        ),
    )

    @admin.display(description="Latest message")
    def message_preview(self, obj):
        text = obj.last_message or ""
        return text[:60] + ("…" if len(text) > 60 else "") or "—"
