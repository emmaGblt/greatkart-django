from .models import Cart, CartItem


def _get_session_key(request):
    """Return the request session key or create one"""
    session = request.session

    if not session.session_key:
        session.create()
    return session.session_key


def get_cart_amounts(cart_items=None):
    """Calculate and return cart amounts (total price, tax and total price with tax)"""
    total_price = 0

    if cart_items:
        for cart_item in cart_items:
            total_price += cart_item.quantity * cart_item.product.price

    tax = round(0.2 * total_price, 2)  # we apply a 2% tax
    total_with_tax = total_price + tax

    return {"total_price": total_price, "tax": tax, "total_with_tax": total_with_tax}


def transfer_cart_to_user(cart, user):
    """Transfer the cart contents to the user. If the user already has a cart, transfer the items one by one
    and delete the cart. Otherwise transfer the cart directly to the user."""

    # Retrieve the cart items to transfer
    cart_items = CartItem.objects.filter(cart=cart)

    # There are items to transfer in the cart (otherwise, do nothing)
    if cart_items.exists():
        try:
            # If the user already has a cart, add the items to this cart
            user_cart = Cart.objects.get(user=user)

            # Add all the session cart items to the user cart
            for cart_item in cart_items:
                user_cart.add_product(
                    cart_item.product,
                    cart_item.variations.all(),
                    cart_item.quantity,
                )

            cart.delete()
        except Cart.DoesNotExist:
            # If the user does not have a cart yet, transfer the cart to them
            cart.user = user
            cart.save()
