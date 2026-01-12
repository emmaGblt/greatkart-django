from django.core.paginator import Paginator


def paginate_products(products, page_number):
    "Paginates the products to display"
    paginator = Paginator(products, 3)
    paginated_products = paginator.get_page(page_number)

    return paginated_products
