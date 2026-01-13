from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.urls import reverse

from django.http import HttpResponse


def cart(request):
    total_price = 0
    cart_items = None

    try:
        session_key = _get_session_key(request)
        cart = Cart.objects.get(session_key=session_key)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True).select_related(
            "product"
        )

        # Calculate total price
        for cart_item in cart_items:
            total_price += cart_item.quantity * cart_item.product.price
    except Cart.DoesNotExist:
        pass

    tax = round(0.2 * total_price, 2)  # we apply a 2% tax
    total_with_tax = total_price + tax

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "tax": tax,
        "total_with_tax": total_with_tax,
    }
    return render(request, "store/cart.html", context)


def _get_session_key(request):
    session = request.session

    if not session.session_key:
        session.create()
    return session.session_key


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

        return HttpResponse(request.POST)

    # Get the cart or create it
    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_key=session_key)

    # Get or create a CartItem for this product

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)

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
