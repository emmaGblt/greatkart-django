from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.urls import reverse


def register(request):
    if request.method == "POST":
        print("here")
        form = form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = Account.objects.create_user(first_name, last_name, email, password)
            user.phone_number = phone_number
            user.save()

            messages.success(request, "Registration successful")
            return redirect(reverse("register"))
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login(request):
    return render(request, "accounts/login.html")


def logout(request):
    return
