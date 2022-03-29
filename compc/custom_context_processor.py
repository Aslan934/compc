from order.models import Order
from shop.models import Category


def order_items_quantity(request):

    try:
        if request.user.is_authenticated:
            order = Order.objects.get(user=request.user, ordered=False)
        else:
            order = Order.objects.get(
                user=None, session_key=request.session.session_key, ordered=False)
        return {"quantity": order.get_quantity}

    except Order.DoesNotExist:
        order = None
        return {"quantity": 0}


def categories(request):
    return {'categories': Category.objects.order_by('-created_at')}
