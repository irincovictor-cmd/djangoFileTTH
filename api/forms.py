from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    ModelForm for the Contact model.
    Fields are defined on the model; this form handles validation + save().
    """

    class Meta:
        model = Contact
        fields = ["name", "email", "contact"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Your name",
                    "autocomplete": "name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),
            "contact": forms.TextInput(
                attrs={
                    "placeholder": "e.g. 09XX XXX XXXX",
                    "inputmode": "tel",
                    "autocomplete": "tel",
                }
            ),
        }
