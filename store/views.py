from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.views import _get_session_key
from carts.models import CartItem
from django.core.paginator import Paginator


def store(request, category_slug=None):
    products = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True, category=category)
    else:
        products = Product.objects.filter(is_available=True)

    paginator = Paginator(products, 3)
    page_number = request.GET.get("page")
    paginated_products = paginator.get_page(page_number)

    context = {
        "paginated_products": paginated_products,
        "product_count": paginated_products.count,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug=None, product_slug=None):
    product = get_object_or_404(Product, slug=product_slug)
    session_key = _get_session_key(request)
    is_already_in_cart = CartItem.objects.filter(
        cart__session_key=session_key, product=product
    ).exists()

    context = {"product": product, "is_already_in_cart": is_already_in_cart}

    return render(request, "store/product_detail.html", context)
