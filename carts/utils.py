def get_cart_amounts(cart_items=None):
    total_price = 0

    if cart_items:
        for cart_item in cart_items:
            total_price += cart_item.quantity * cart_item.product.price

    tax = round(0.2 * total_price, 2)  # we apply a 2% tax
    total_with_tax = total_price + tax

    return {"total_price": total_price, "tax": tax, "total_with_tax": total_with_tax}
