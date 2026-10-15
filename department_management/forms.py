from django import forms
from .models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["code", "name", "head", "office_location", "date_established"]
        labels = {
            "code": "Department code",
            "name": "Department name",
            "head": "Department head",
            "office_location": "Office location",
            "date_established": "Date established",
        }
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. d1234"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Finance"}),
            "head": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Crizan"}),
            "office_location": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Tawala"}),
            "date_established": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
