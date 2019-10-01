from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = {
            "name",
            "manager_name",
            "website",
            "email",
            "phone",
            "address",
            "description",
            "is_active"
        }