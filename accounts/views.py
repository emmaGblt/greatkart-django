from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account


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
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login(request):
    return render(request, "accounts/login.html")


def logout(request):
    return
