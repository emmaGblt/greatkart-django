from django.shortcuts import render, redirect
from store.models import Product
from carts.models import Cart, CartItem
from django.urls import reverse
from django.db.models import Sum


def cart(request):
    total_price = 0
    cart_items = None

    try:
        session_key = _get_session_key(request)
        cart = Cart.objects.get(session_key=session_key)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # Calculate total price
        total_price = cart_items.aggregate(
            total_price=Sum("product__price", default=0)
        )["total_price"]
    except Cart.DoesNotExist:
        pass

    tax = 0.2 * total_price  # we apply a 2% tax
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
    product = Product.objects.get(id=product_id)
    session_key = _get_session_key(request)

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
