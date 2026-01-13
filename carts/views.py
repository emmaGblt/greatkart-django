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

    request_variations = []

    if request.method == "POST":
        for key, value in request.POST.items():
            try:
                # Check if a variation exists for this key-value pair
                variation = Variation.objects.get(
                    product=product, category=key, value=value
                )
                request_variations.append(variation)
            except Variation.DoesNotExist:
                pass

    # Get the cart or create it
    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_key=session_key)

    # Get or create a new CartItem for this product
    request_variations_ids = [var.id for var in request_variations]
    cart_item_with_same_variations = None

    # Find all the CartItem instances for this product and this cart
    cart_items = CartItem.objects.filter(cart=cart, product=product)

    # Loop through the cart items to find one with the same variations as those passed in the request
    for ci in cart_items:
        ci_variation_ids = ci.variations.values_list("id", flat=True)
        if sorted(ci_variation_ids) == sorted(request_variations_ids):
            # A cart item with the same variations has been found
            cart_item_with_same_variations = ci
            break

    # If a cart item with the same variations has been found, increase its quantity by one
    if cart_item_with_same_variations:
        cart_item = cart_item_with_same_variations
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Else, create a new cart item with the request variations
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
        cart_item.variations.set(request_variations)
        cart_item.save()

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
