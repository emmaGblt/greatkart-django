from django.urls import path
from . import views


urlpatterns = [
    path("", views.cart, name="cart"),
    path(
        "add-product-to-cart/<int:product_id>/",
        views.add_product_to_cart,
        name="add-product-to-cart",
    ),
    path(
        "decrement-product-from-cart-item/<int:cart_item_id>",
        views.decrement_product_from_cart_item,
        name="decrement-product-from-cart-item",
    ),
    path(
        "increment-product-from-cart-item/<int:cart_item_id>",
        views.increment_product_from_cart_item,
        name="increment-product-from-cart-item",
    ),
    path(
        "delete-cart-item/<int:cart_item_id>",
        views.delete_cart_item,
        name="delete-cart-item",
    ),
    path("checkout/", views.checkout, name="checkout"),
]
