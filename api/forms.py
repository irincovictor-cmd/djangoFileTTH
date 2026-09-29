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
    """Modal form: add a topic and optionally remove an existing one."""

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
    remove_topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        required=False,
        label="Remove old topic",
        empty_label="— None (just add) —",
        help_text="Optional: delete this topic when adding the new one.",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
