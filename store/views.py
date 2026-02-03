from django.shortcuts import render, get_object_or_404, redirect

from store.forms import ProductReviewForm
from .models import Product, ProductReview
from category.models import Category
from django.db.models import Q
from .utils import paginate_products
from django.contrib import messages


def store(request, category_slug=None):
    products = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True, category=category)
    else:
        products = Product.objects.filter(is_available=True)

    page_number = request.GET.get("page")
    paginated_products = paginate_products(products, page_number)

    context = {
        "paginated_products": paginated_products,
        "product_count": paginated_products.paginator.count,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug=None, product_slug=None):
    product = get_object_or_404(Product, slug=product_slug)

    product_review_form = ProductReviewForm()

    context = {"product": product, "product_review_form": product_review_form}

    return render(request, "store/product_detail.html", context)


def search(request):
    search_value = request.GET.get("search", None)

    if search_value:
        products = Product.objects.filter(
            Q(description__icontains=search_value) | Q(name__icontains=search_value)
        )
    else:
        products = Product.objects.all()

    page_number = request.GET.get("page")
    paginated_products = paginate_products(products, page_number)

    context = {
        "paginated_products": paginated_products,
        "product_count": paginated_products.paginator.count,
    }
    return render(request, "store/store.html", context)


def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    url = request.META.get("HTTP_REFERER")

    if request.method == "POST":
        try:
            product_review = ProductReview.objects.get(user=user, product=product)

            # Update existing review
            form = ProductReviewForm(request.POST, instance=product_review)
            form.save()
            messages.success(request, "Your review has been successfully updated!")
            return redirect(url)
        except ProductReview.DoesNotExist:
            form = ProductReviewForm(request.POST)
            if form.is_valid():
                ProductReview.objects.create(
                    product=product,
                    user=user,
                    title=form.cleaned_data["title"],
                    content=form.cleaned_data["content"],
                    rating=form.cleaned_data["rating"],
                )
                messages.success(
                    request, "Thank you, your review has been successfully submitted!"
                )
                return redirect(url)
