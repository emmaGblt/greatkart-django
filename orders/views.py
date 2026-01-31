from django.shortcuts import redirect, render, get_list_or_404
from django.contrib.auth.decorators import login_required
from carts.models import CartItem
from django.urls import reverse
from django.contrib import messages

from carts.utils import get_cart_amounts
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import json
from django.core.exceptions import ValidationError


@login_required
def place_order(request):
    user = request.user

    cart_items = CartItem.objects.filter(cart__user=user)

    # If no cart items, redirect to the store
    if not cart_items.exists():
        return redirect(reverse("store"))

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order_amounts = get_cart_amounts(cart_items)
            # Create order instance
            Order.objects.create(
                user=user,
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                phone_number=form.cleaned_data["phone_number"],
                address_line_1=form.cleaned_data["address_line_1"],
                address_line_2=form.cleaned_data["address_line_2"],
                state=form.cleaned_data["state"],
                city=form.cleaned_data["city"],
                country=form.cleaned_data["country"],
                note=form.cleaned_data["note"],
                total=order_amounts["total_with_tax"],
                tax=order_amounts["tax"],
                ip=request.META.get("REMOTE_ADDR"),
            )

            return redirect(reverse("payments"))
        else:
            return redirect(reverse("checkout"))
    else:
        return redirect(reverse("checkout"))


@login_required
def payments(request):
    user = request.user
    if request.method == "POST":
        body = json.loads(request.body)
        try:
            # Retrieve the corresponding order
            order = Order.objects.get(
                user=user,
                status=Order.STATUS_CHOICES["new"],
                reference=body.get("order_reference"),
            )

            # Create the payment instance
            payment = Payment(
                method=Payment.METHOD_CHOICES.get(body.get("payment_method")),
                amount=order.total,
                transaction_id=body.get("transaction_id"),
                status=body.get("status"),
            )
            payment.full_clean()  # Allows to check the method value
            payment.save()

            # Update the order instance
            order.payment = payment
            order.status = Order.STATUS_CHOICES["completed"]
            order.save()

            # Create the order products
            cart_items = CartItem.objects.filter(cart__user=user).select_related(
                "product"
            )

            for cart_item in cart_items:
                new_order_product = OrderProduct.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                )
                if cart_item.variations.exists():
                    new_order_product.variations.set(cart_item.variations.all())

            cart_items.delete()

            # Update the product quantities

            # Clear the cart

            # Send email

            # Send JSON response to JS method savePaymentData
            messages.success(request, "Order completed successfully!")
            return redirect(reverse("payments"))
        except (Order.DoesNotExist, ValidationError) as e:
            messages.error(request, "Ooops! Something went wrong...")
            print(e)
            # FIXME: Cancel payment?
            return redirect(reverse("payments"))
    else:
        orders = get_list_or_404(Order, user=user, status=Order.STATUS_CHOICES["new"])
        order = orders[0]

        cart_items = CartItem.objects.filter(cart__user=user)
        order_amounts = get_cart_amounts(cart_items)

        context = {
            "order": order,
            "total_price": order_amounts["total_price"],
            "tax": order_amounts["tax"],
            "total_with_tax": order_amounts["total_with_tax"],
            "cart_items": cart_items,
        }

        return render(request, "orders/payments.html", context)
