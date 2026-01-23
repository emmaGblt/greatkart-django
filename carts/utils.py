from .models import Cart, CartItem


def _get_session_key(request):
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


def merge_cart_item_into_cart_items(new_cart_item, cart, cart_items):
    """If a cart item with the same product and variations alreadt exists in the cart, increase its quantity.
    Otherwise, add the cart item to the cart"""

    cart_item_with_same_variations_exists = False

    # Check if cart items with the same product exist
    same_product_cart_items = cart_items.filter(product=new_cart_item.product)

    # If True, look for a cart item with the same variations
    if same_product_cart_items.exists():
        new_cart_item_variations_ids = new_cart_item.variations.values_list(
            "id", flat=True
        )  # the ids of the new cart item variations

        for same_product_cart_item in same_product_cart_items:
            same_product_cart_item_variations_ids = (
                same_product_cart_item.variations.values_list("id", flat=True)
            )  # the ids of the cart item variations

            # Compare the variation ids
            if sorted(same_product_cart_item_variations_ids) == sorted(
                new_cart_item_variations_ids
            ):
                # Increase the quantity of the cart item
                same_product_cart_item.quantity += new_cart_item.quantity
                same_product_cart_item.save()
                cart_item_with_same_variations_exists = True
                break

    # If no cart item with the same variations, just add the new cart item to the cart
    if not cart_item_with_same_variations_exists:
        new_cart_item.cart = cart
        new_cart_item.save()


def transfer_cart_items_to_user(request, user):
    session_key = _get_session_key(request)

    session_cart_items = CartItem.objects.filter(cart__session_key=session_key)

    print(session_cart_items.exists())

    # There are items in the cart for the anonymous session (otherwise, do nothing)
    if session_cart_items.exists():
        session_cart = Cart.objects.get(session_key=session_key)

        try:
            # If the user already has a cart, add the items to this cart
            user_cart = Cart.objects.get(user=user)
            user_cart_items = CartItem.objects.filter(cart=user_cart).select_related(
                "product"
            )

            for session_cart_item in session_cart_items:
                merge_cart_item_into_cart_items(
                    session_cart_item, user_cart, user_cart_items
                )

        except Cart.DoesNotExist:
            # If the user does not have a cart yet, transfer the session cart to them
            session_cart.user = user
            session_cart.save()
