from django.db import models
from accounts.models import Account
from store.models import Product, Variation
import uuid


class Payment(models.Model):
    PAYPAL = "paypal"
    METHOD_CHOICES = {
        PAYPAL: "paypal",
    }  # Add other methods later

    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=100)  # FIXME: pas très clair ce que c'est
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} ({self.method})"


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

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_products"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="+")
    variations = models.ManyToManyField(Variation, blank=True, related_name="+")
    price = models.IntegerField()  # In case the product price has changed
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} (order: {1})".format(self.product.name, self.order.reference)
