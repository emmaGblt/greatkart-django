from django.db import models
from accounts.models import Account
from store.models import Product, Variation
import uuid


class Payment(models.Model):
    method = models.CharField(max_length=100)  # FIXME: un choice serait mieux non ?
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=100)  # FIXME: un choice !
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class Order(models.Model):
    NEW = "new"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    STATUS_CHOICES = {
        NEW: "new",
        ACCEPTED: "accepted",
        COMPLETED: "completed",
        CANCELLED: "cancelled",
    }

    reference = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name="orders"
    )
    payment = models.OneToOneField(
        Payment, on_delete=models.SET_NULL, blank=True, null=True, related_name="order"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    note = models.CharField(max_length=100, blank=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    tax = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES["new"]
    )
    ip = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Order {0} ({1} {2})".format(
            self.reference, self.first_name, self.last_name
        )


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_products"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="+")
    variation = models.ManyToManyField(Variation, blank=True, related_name="+")
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} (order: {1})".format(self.product.name, self.order.id)
