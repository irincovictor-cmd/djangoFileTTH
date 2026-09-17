from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """Portfolio / site contact form → saves to Contact table."""

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
