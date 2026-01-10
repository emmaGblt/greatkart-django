from .models import CartItem
from .views import _get_session_key
from django.db.models import Sum


def cart_items_count(request):
    session_key = _get_session_key(request)
    cart_items_count = CartItem.objects.filter(cart__session_key=session_key).aggregate(
        total=Sum("quantity", default=0)
    )["total"]

    return dict(cart_items_count=cart_items_count)
