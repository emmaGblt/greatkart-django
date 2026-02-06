from django.contrib import admin
from .models import Account, UserProfile

from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.html import format_html


class AccountCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Account
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "is_admin",
            "is_active",
        ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
            "is_active",
            "is_admin",
        ]


@admin.register(Account)
class AccountAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = AccountChangeForm
    add_form = AccountCreationForm

    list_display = [
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_admin",
        "is_active",
    ]
    list_filter = ["is_admin"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["-date_joined"]

    readonly_fields = ["last_login", "date_joined", "is_superuser"]

    filter_horizontal = []
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Personal info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "phone_number",
                    "is_active",
                    "date_joined",
                    "last_login",
                ]
            },
        ),
        ("Permissions", {"fields": ["is_admin", "is_superuser"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "is_active",
                    "is_admin",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "state", "country", "thumbnail"]

    @admin.display(description="User profile pic.")
    def thumbnail(self, object):
        return format_html(
            "<img src={} width='30' height='30' style='border-radius:50%;' />",
            object.picture.url,
        )
