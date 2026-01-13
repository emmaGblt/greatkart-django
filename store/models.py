from django.db import models
from category.models import Category
from django.urls import reverse


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
        return reverse("product_detail", args=[self.category.slug, self.slug])

    class Meta:
        ordering = ["-created_at"]


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    COLOR = "color"
    SIZE = "size"
    CATEGORY_CHOICES = {COLOR: "color", SIZE: "size"}
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product)
