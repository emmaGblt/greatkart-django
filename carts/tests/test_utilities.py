import pytest
from accounts.factories import AccountFactory
from carts.factories import CartFactory, CartItemFactory
from carts.models import Cart, CartItem
from store.factories import ProductFactory
from carts.utils import get_cart_amounts, transfer_cart_to_user


@pytest.mark.django_db
def test_get_cart_amounts():
    # Create an empty cart
    cart = CartFactory()

    # Get the empty cart amounts
    amounts = get_cart_amounts(CartItem.objects.filter(cart=cart))

    # Check that everything is equal to 0
    assert amounts["total_price"] == 0
    assert amounts["tax"] == 0
    assert amounts["total_with_tax"] == 0

    # Add cart items to the cart
    product_1 = ProductFactory(price=10.0)
    CartItemFactory(cart=cart, product=product_1, quantity=2)

    product_2 = ProductFactory(price=20.0)
    CartItemFactory(cart=cart, product=product_2, quantity=3)

    # Get the cart amounts
    amounts = get_cart_amounts(CartItem.objects.filter(cart=cart))

    # The expected results
    expected_total_price = 10.0 * 2 + 20.0 * 3
    expected_tax = round(0.2 * expected_total_price, 2)  # 2% tax

    # Check that the amounts correspond to the expected results
    assert amounts["total_price"] == expected_total_price
    assert amounts["tax"] == expected_tax
    assert amounts["total_with_tax"] == expected_total_price + expected_tax


@pytest.mark.django_db
def test_transfer_cart_to_user():
    # Create a user
    user = AccountFactory()

    # Create an anonymous cart
    cart = CartFactory(user=None)

    # Transfer the empty cart to the user
    transfer_cart_to_user(cart, user)

    # Check that nothing happened
    assert cart.user is None
    assert hasattr(user, "cart") is False

    # Create cart items
    CartItemFactory(cart=cart)
    CartItemFactory(cart=cart)

    # Check the cart content
    assert cart.cart_items.count() == 2

    # Transfer the cart contents to the user
    transfer_cart_to_user(cart, user)

    # Check that the cart has been transfered directly to the user
    assert cart.user == user
    assert user.cart == cart
    assert cart.cart_items.count() == 2

    # Create a new cart with cart items
    cart_2 = CartFactory(user=None)
    CartItemFactory(cart=cart_2)
    CartItemFactory(cart=cart_2)

    # Transfer the cart contents to the user (user has a cart now)
    transfer_cart_to_user(cart_2, user)

    # Check that the cart has been deleted and its content transfered
    assert user.cart.cart_items.count() == 4
    with pytest.raises(Cart.DoesNotExist):
        cart_2.refresh_from_db()
