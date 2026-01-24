from django.db import models
from store.models import Product, Variation
from accounts.models import Account
from django.db.models import Q


class Cart(models.Model):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, null=True, default=None
    )
    session_key = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session_key}"

    def add_product(self, product, variations=[], quantity=1):
        """Add a product and its variations to the cart by creating or updating a cart item."""
        filters = Q(product=product)

        # Handle product with no variations
        if not variations:
            filters &= Q(variations=None)

        # Find the existing cart items with the same product
        same_product_cart_items = self.cart_items.filter(filters)
        same_cart_item_exists = False

        if same_product_cart_items.exists():
            sorted_variation_ids = sorted([variation.id for variation in variations])

            # Loop through the cart items to find one with the same variations
            for same_product_cart_item in same_product_cart_items:
                same_product_cart_item_variation_ids = (
                    same_product_cart_item.variations.values_list("id", flat=True)
                )

                # A cart item with the same variations has been found
                if sorted_variation_ids == sorted(same_product_cart_item_variation_ids):
                    same_product_cart_item.quantity += quantity
                    same_product_cart_item.save()
                    same_cart_item_exists = True
                    break

        if not same_cart_item_exists:
            # Create a new cart item with the corresponding product and variations
            new_cart_item = CartItem.objects.create(
                cart=self, product=product, quantity=quantity
            )
            if variations:
                new_cart_item.variations.set(variations)
                new_cart_item.save()


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
