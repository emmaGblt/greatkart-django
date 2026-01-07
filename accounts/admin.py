from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ["email", "first_name", "last_name", "is_admin"]
    list_filter = []
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["-date_joined"]

    readonly_fields = ["last_login", "date_joined"]

    filter_horizontal = []
    fieldsets = []
