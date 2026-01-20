from django import forms
from .models import Account
import re


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"})
    )

    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password",
            "confirm_password",
        ]
        widgets = {
            "password": forms.PasswordInput(attrs={"placeholder": "Enter password"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Fist name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Phone number"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        pattern = r"^[0-9]{10}$"
        if not re.match(pattern, phone_number):
            raise forms.ValidationError("Your phone number has an invalid format!")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        confirm_password = cleaned_data["confirm_password"]

        if password != confirm_password:
            raise forms.ValidationError("Confirmation password does not match.")
        return cleaned_data
