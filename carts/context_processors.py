from .models import CartItem
from .utils import _get_session_key
from django.db.models import Sum
from django.db.models import Q


def cart_items_count(request):
    user = request.user
    if user.is_authenticated:
        filter = Q(cart__user=user)
    else:
        session_key = _get_session_key(request)
        filter = Q(cart__session_key=session_key)

    cart_items_count = CartItem.objects.filter(filter).aggregate(
        total=Sum("quantity", default=0)
    )["total"]

    return dict(cart_items_count=cart_items_count)
