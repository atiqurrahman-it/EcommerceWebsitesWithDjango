from django.shortcuts import render
from .forms import BillingForm
from App_Order.models import Order


# Create your views here.

def Checkout(request):
    form = BillingForm()
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderItems.all()
    order_total_price = order_qs[0].get_totals()
    print(order_items)
    data = {
        "title": 'checkout page',
        "form": form,
        "single_orders": order_items,
        "order_total": order_total_price,
    }
    return render(request, 'payment/Checkout.html', data)
