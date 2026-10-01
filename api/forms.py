from django import forms
from .models import Contact, Topic


class ContactForm(forms.ModelForm):
    """Shared name/email/message fields for LearnHub and Portfolio forms."""

    class Meta:
        model = Contact
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Your name",
                    "autocomplete": "name",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                    "class": "form-control",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Your message",
                    "rows": 5,
                    "class": "form-control",
                }
            ),
        }


class TopicManageForm(forms.Form):
    """Add-topic modal only (no delete here — use Edit topic for move to bin)."""

    title = forms.CharField(
        max_length=200,
        label="Topic name",
        widget=forms.TextInput(attrs={"placeholder": "e.g. What is Django?", "class": "form-control"}),
    )
    tag = forms.CharField(
        max_length=50,
        label="Category",
        widget=forms.TextInput(attrs={"placeholder": "e.g. Basics, Routing", "class": "form-control"}),
    )
    summary = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Short description shown on the topics list",
                "rows": 3,
                "class": "form-control",
            }
        ),
    )
    body = forms.CharField(
        label="Full body (optional)",
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Longer text for the detail page (defaults to description)",
                "rows": 4,
                "class": "form-control",
            }
        ),
    )
    resource_url = forms.URLField(
        label="Learn more link (optional)",
        required=False,
        widget=forms.URLInput(
            attrs={
                "placeholder": "https://docs.djangoproject.com/...",
                "class": "form-control",
            }
        ),
        help_text="External URL for students who want to study more on this topic.",
    )
    resource_label = forms.CharField(
        max_length=100,
        label="Link label (optional)",
        required=False,
        initial="Learn more",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Learn more",
                "class": "form-control",
            }
        ),
    )


class TopicEditForm(forms.ModelForm):
    """Edit an existing active topic.

    Idea adapted from reference topic_edit (Hannah): load → form → save.
    Soft-delete (move to bin) is offered on the edit page, not on Add.
    """

    class Meta:
        model = Topic
        fields = [
            "title",
            "tag",
            "summary",
            "body",
            "resource_url",
            "resource_label",
        ]
        labels = {
            "title": "Topic name",
            "tag": "Category",
            "summary": "Description",
            "body": "Full body",
            "resource_url": "Learn more link",
            "resource_label": "Link label",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "e.g. What is Django?", "class": "form-control"}
            ),
            "tag": forms.TextInput(
                attrs={"placeholder": "e.g. Basics, Routing", "class": "form-control"}
            ),
            "summary": forms.Textarea(
                attrs={
                    "placeholder": "Short description on the topics list",
                    "rows": 3,
                    "class": "form-control",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "placeholder": "Longer text for the detail page",
                    "rows": 5,
                    "class": "form-control",
                }
            ),
            "resource_url": forms.URLInput(
                attrs={
                    "placeholder": "https://docs.djangoproject.com/...",
                    "class": "form-control",
                }
            ),
            "resource_label": forms.TextInput(
                attrs={"placeholder": "Learn more", "class": "form-control"}
            ),
        }
