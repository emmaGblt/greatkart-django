import pytest
from carts.factories import CartFactory, CartItemFactory
from store.factories import ProductFactory, VariationFactory
from store.models import Variation


@pytest.mark.django_db
def test_add_product():
    # Create a cart
    cart = CartFactory()

    # Create products
    product_1 = ProductFactory()
    product_2 = ProductFactory()

    # Check cart is empty
    assert cart.cart_items.count() == 0

    # Add product in empty cart
    cart.add_product(product_1)

    # Check that a new cart item has been created (default quantity is 1)
    assert cart.cart_items.count() == 1
    cart_item = cart.cart_items.first()
    assert cart_item.product == product_1
    assert cart_item.quantity == 1
    assert cart_item.variations.count() == 0

    # Add same product without variations with specified quantity
    cart.add_product(product_1, quantity=3)

    # Check that corresponding cart item quantity has been increased
    assert cart.cart_items.count() == 1
    cart_item = cart.cart_items.first()
    assert cart_item.product == product_1
    assert cart_item.quantity == 4
    assert cart_item.variations.count() == 0

    # Create variations
    variation_1 = VariationFactory(
        product=product_2, category=Variation.CATEGORY_CHOICES["color"], value="blue"
    )
    variation_2 = VariationFactory(
        product=product_2, category=Variation.CATEGORY_CHOICES["size"], value="small"
    )
    variation_3 = VariationFactory(
        product=product_2, category=Variation.CATEGORY_CHOICES["color"], value="gray"
    )

    # Create a cart item with some variations
    cart_item_with_variations_1 = CartItemFactory(
        cart=cart, product=product_2, quantity=1, variations=[variation_1, variation_2]
    )

    # Check the number of cart items
    assert cart.cart_items.count() == 2

    # Add same product with the same variations
    cart.add_product(product_2, [variation_1, variation_2], quantity=2)

    # Check that corresponding cart item quantity has been increased (no new cart item has been created)
    assert cart.cart_items.count() == 2  # same number of cart items
    cart_item_with_variations_1.refresh_from_db()
    assert cart_item_with_variations_1.quantity == 3
    assert sorted(
        cart_item_with_variations_1.variations.values_list("id", flat=True)
    ) == sorted([variation_1.id, variation_2.id])

    # Add same product with different variations
    cart.add_product(product_2, [variation_2, variation_3], quantity=4)

    # Check that a new cart item has been created
    assert cart.cart_items.count() == 3
    cart_item_with_variations_2 = cart.cart_items.last()
    assert cart_item_with_variations_2.product == product_2
    assert cart_item_with_variations_2.quantity == 4
    assert sorted(
        cart_item_with_variations_2.variations.values_list("id", flat=True)
    ) == sorted([variation_2.id, variation_3.id])

    # Check that the previous cart item is unchanged
    cart_item_with_variations_1.refresh_from_db()
    assert cart_item_with_variations_1.quantity == 3

    # Add same product without variations
    cart.add_product(product_2)

    # Check that a new cart item has been created
    assert cart.cart_items.count() == 4
    cart_item_with_variations_3 = cart.cart_items.last()
    assert cart_item_with_variations_3.product == product_2
    assert cart_item_with_variations_3.quantity == 1
    assert not cart_item_with_variations_3.variations.all()

    # Check that the previous cart item is unchanged
    cart_item_with_variations_2.refresh_from_db()
    assert cart_item_with_variations_2.quantity == 4
