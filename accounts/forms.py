from django import forms
from .models import Account


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
