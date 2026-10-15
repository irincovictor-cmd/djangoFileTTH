from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["employee_id", "name", "email", "position", "department", "hire_date"]
        labels = {
            "employee_id": "Employee ID",
            "name": "Full name",
            "email": "Email",
            "position": "Position",
            "department": "Department",
            "hire_date": "Hire date",
        }
        widgets = {
            "employee_id": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. EMP001"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-control"}),
            "hire_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
