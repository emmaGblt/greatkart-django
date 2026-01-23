import pytest
from carts.factories import CartFactory, CartItemFactory
from carts.models import CartItem
from store.factories import ProductFactory
from carts.utils import get_cart_amounts


@pytest.mark.django_db
def test_get_cart_amounts():
    # Cart with no cart items
    cart_1 = CartFactory()

    amounts = get_cart_amounts(CartItem.objects.filter(cart=cart_1))

    assert amounts["total_price"] == 0
    assert amounts["tax"] == 0
    assert amounts["total_with_tax"] == 0

    # Cart with cart items
    cart_2 = CartFactory()

    # Cart item 1
    product_1 = ProductFactory(price=10.0)
    CartItemFactory(cart=cart_2, product=product_1, quantity=2)

    # Cart item 2
    product_2 = ProductFactory(price=20.0)
    CartItemFactory(cart=cart_2, product=product_2, quantity=3)

    amounts = get_cart_amounts(CartItem.objects.filter(cart=cart_2))
    expected_total_price = 10.0 * 2 + 20.0 * 3
    expected_tax = round(0.2 * expected_total_price, 2)  # 2% tax

    assert amounts["total_price"] == expected_total_price
    assert amounts["tax"] == expected_tax
    assert amounts["total_with_tax"] == expected_total_price + expected_tax
