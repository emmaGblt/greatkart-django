from django.shortcuts import render
from .models import Product


def store(request):
    products = Product.objects.filter(is_available=True)

    context = {
        "products": products,
        "product_count": products.count(),
    }
    return render(request, "store/store.html", context)
