from django.contrib import admin
from .models import Topic, Contact, Profile


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "resource_url", "created_at")
    search_fields = ("title", "tag", "summary")


class ContactInline(admin.TabularInline):
    """Show all contact-form uses under a Profile."""

    model = Contact
    extra = 0
    readonly_fields = ("name", "email", "message", "created_at")
    can_delete = True
    show_change_link = True


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
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
    readonly_fields = ("contact_count", "last_contact_at", "created_at", "updated_at")
    inlines = [ContactInline]
    fieldsets = (
        (None, {"fields": ("name", "email", "user", "notes")}),
        (
            "Contact page usage",
            {"fields": ("contact_count", "last_contact_at", "created_at", "updated_at")},
        ),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "profile", "message_preview", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    autocomplete_fields = ("profile",)

    @admin.display(description="Message")
    def message_preview(self, obj):
        text = obj.message or ""
        return text[:60] + ("…" if len(text) > 60 else "")
