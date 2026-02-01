from django.contrib import admin
from .models import Product, ProductReview, Variation


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "stock", "category", "updated_at", "is_available"]

    prepopulated_fields = {"slug": ["name"]}


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ["product", "category", "value", "is_active"]
    list_filter = ["category", "is_active"]
    list_editable = ["is_active"]


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass
