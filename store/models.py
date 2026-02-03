from django.db import models
from accounts.models import Account
from category.models import Category
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="photos/products")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse("product-detail", args=[self.category.slug, self.slug])

    class Meta:
        ordering = ["-created_at"]


class VariationManager(models.Manager):
    def colors(self):
        return self.filter(category=Variation.COLOR, is_active=True)

    def sizes(self):
        return self.filter(category=Variation.SIZE, is_active=True)


class Variation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variations"
    )

    COLOR = "color"
    SIZE = "size"
    CATEGORY_CHOICES = {COLOR: "color", SIZE: "size"}
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return f"{self.product} ({self.category}: {self.value})"


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_reviews"
    )
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="product_reviews"
    )
    title = models.CharField(max_length=100, blank=True)
    content = models.CharField(max_length=500, blank=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} ({self.user})"
