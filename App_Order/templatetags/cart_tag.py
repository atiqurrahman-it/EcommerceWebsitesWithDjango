from django import template
from App_Order.models import Order

register = template.Library()


@register.filter
def total_Cart_or_order_items(user):
    order = Order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].orderItems.count()
    else:
        return 0
