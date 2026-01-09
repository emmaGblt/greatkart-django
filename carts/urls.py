from django.urls import path
from . import views


urlpatterns = [
    path("", views.cart, name="cart"),
    path(
        "add_product_to_cart/<int:product_id>/",
        views.add_product_to_cart,
        name="add_product_to_cart",
    ),
    path(
        "decrement_product_from_cart_item/<int:cart_item_id>",
        views.decrement_product_from_cart_item,
        name="decrement_product_from_cart_item",
    ),
    path(
        "increment_product_from_cart_item/<int:cart_item_id>",
        views.increment_product_from_cart_item,
        name="increment_product_from_cart_item",
    ),
    path(
        "delete_cart_item/<int:cart_item_id>",
        views.delete_cart_item,
        name="delete_cart_item",
    ),
]
