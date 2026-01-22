from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def register(request):
    if request.method == "POST":
        form = form = RegistrationForm(request.POST)
        if form.is_valid():
            # GET THE DATA FROM THE FORM
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # CREATE A USER
            user = Account.objects.create_user(first_name, last_name, email, password)
            user.phone_number = phone_number
            user.save()

            # SEND A LINK TO ACTIVATE THE USER (= EMAIL ADDurlsafe_base64_decodeRESS VALIDATION)
            current_site = get_current_site(request)
            token = default_token_generator.make_token(user)
            mail_subject = "Account activation"
            mail_message = render_to_string(
                "accounts/verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": token,
                },
            )
            recipient_email = email
            send_mail(
                mail_subject, mail_message, None, recipient_list=[recipient_email]
            )

            return redirect(
                reverse("login", query={"status": "verification", "email": email})
            )
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Handle redirection after login when a view has the login_required decorator (for instance)
        next = request.POST.get("next")

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(next or reverse("home"))
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect(reverse("login"))

    return render(request, "accounts/login.html")


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out!")
    return redirect(reverse("login"))


def activate_account(request, uidb64, token):
    try:
        pk = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if user.is_active:
            messages.error(
                request, "Your account has already been activated! Please login."
            )
            return redirect(reverse("login"))
        else:
            user.is_active = True
            user.save()
            messages.success(request, "Your account is now activated!")
            return redirect(reverse("login"))
    else:
        messages.error(request, "Account activation failed...")
        return redirect(reverse("register"))


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")
