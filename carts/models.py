from django.db import models
from store.models import Product, Variation
from accounts.models import Account


class Cart(models.Model):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, null=True, default=None
    )
    session_key = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session_key}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True, related_name="+")
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} (cart: {self.cart.session_key})"

    def total_price(self):
        return self.product.price * self.quantity
