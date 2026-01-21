from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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

            messages.success(request, "Registration successful!")
            return redirect(reverse("register"))
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            # messages.success(request, "Login successful!")
            return redirect(reverse("home"))
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect(reverse("login"))

    return render(request, "accounts/login.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out!")
    return redirect(reverse("login"))
