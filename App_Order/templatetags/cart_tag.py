from django import template
from App_Order.models import Card

register = template.Library()


@register.filter
def total_Cart_or_order_items(user):
    order = Card.objects.filter(user=user, purchased=False)
    if order.exists():
        return order.count()
    else:
        return 0
