from django.shortcuts import render, redirect

from carts.models import Cart
from orders.models import Order
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
from carts.utils import _get_session_key, transfer_cart_to_user


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

            # SEND A LINK TO ACTIVATE THE USER (= EMAIL ADDRESS VALIDATION)
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
            # Transfer the cart items from the anonymous session cart to the user cart
            session_key = _get_session_key(request)
            try:
                session_cart = Cart.objects.get(session_key=session_key)
                transfer_cart_to_user(session_cart, user)
            except Cart.DoesNotExist:
                pass

            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect(next or reverse("dashboard"))
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
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
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
    user = request.user

    orders_count = Order.objects.filter(
        user=user, status=Order.STATUS_CHOICES["completed"]
    ).count()

    context = {"orders_count": orders_count}
    return render(request, "accounts/dashboard.html", context)


def index(request):
    return redirect(reverse("dashboard"))


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            user = None

        if user:
            # SEND A LINK TO RESET THE PASSWORD
            current_site = get_current_site(request)
            token = default_token_generator.make_token(user)
            mail_subject = "Password reset"
            mail_message = render_to_string(
                "accounts/reset_password_email.html",
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
            messages.success(
                request, "A reset password link has been sent to your email address."
            )
            redirect(reverse("login"))
        else:
            messages.error(request, "Account with this email does not exist.")
            return redirect(reverse("forgot-password"))

    return render(request, "accounts/forgot_password.html")


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # FIXME: Check if the account has already been activated or not?
        # Store the ui in the session
        request.session["uid"] = uid
        return redirect(reverse("reset-password"))
    else:
        messages.error(request, "Password reset failed...")
        return redirect(reverse("login"))


def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            try:
                uid = request.session.get("uid")
                user = Account.objects.get(id=uid)

                user.set_password(password)
                user.save()
                messages.success(request, "Your password has been successfully reset!")
            except Account.DoesNotExist:
                messages.error(request, "Ooops! Something went wrong...")

            return redirect(reverse("login"))
        else:
            messages.error(request, "Passwords do not match!")
            return redirect(reverse("reset-password"))
    return render(request, "accounts/reset_password.html")


@login_required
def my_orders(request):
    user = request.user

    orders = Order.objects.filter(user=user, status=Order.STATUS_CHOICES["completed"])

    context = {"orders": orders}
    return render(request, "accounts/my_orders.html", context)


@login_required
def edit_profile(request):
    return render(request, "accounts/edit_profile.html")
