from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.urls import reverse
from .utils import get_cart_amounts, _get_session_key
from django.contrib.auth.decorators import login_required


def cart(request):
    cart_items = None

    try:
        session_key = _get_session_key(request)
        cart = Cart.objects.get(session_key=session_key)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True).select_related(
            "product"
        )
    except Cart.DoesNotExist:
        pass

    cart_amounts = get_cart_amounts(cart_items)

    context = {
        "cart_items": cart_items,
        "total_price": cart_amounts["total_price"],
        "tax": cart_amounts["tax"],
        "total_with_tax": cart_amounts["total_with_tax"],
    }
    return render(request, "store/cart.html", context)


def add_product_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = _get_session_key(request)

    variations = []

    if request.method == "POST":
        for key, value in request.POST.items():
            try:
                # Check if a variation exists for this key-value pair
                variation = Variation.objects.get(
                    product=product, category=key, value=value
                )
                variations.append(variation)
            except Variation.DoesNotExist:
                pass

    # Get the cart or create it
    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_key=session_key)

    cart.add_product(product, variations, quantity=1)

    return redirect(reverse("cart"))


def increment_product_from_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    cart_item.quantity += 1
    cart_item.save()

    return redirect(reverse("cart"))


def decrement_product_from_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect(reverse("cart"))


def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()

    return redirect(reverse("cart"))


@login_required
def checkout(request):
    cart_items = None

    try:
        session_key = _get_session_key(request)
        cart = Cart.objects.get(session_key=session_key)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True).select_related(
            "product"
        )
    except Cart.DoesNotExist:
        pass

    cart_amounts = get_cart_amounts(cart_items)

    context = {
        "cart_items": cart_items,
        "total_price": cart_amounts["total_price"],
        "tax": cart_amounts["tax"],
        "total_with_tax": cart_amounts["total_with_tax"],
    }
    return render(request, "store/checkout.html", context)
