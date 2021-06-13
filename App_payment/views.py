from django.shortcuts import render
from .forms import BillingForm
from App_Order.models import Order
from .models import BillingAddress
from django.contrib import messages


# Create your views here.

def Checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request, f"shipping Address Saved !")
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderItems.all()
    order_total_price = order_qs[0].get_totals()
    data = {
        "title": 'checkout page',
        "form": form,
        "single_orders": order_items,
        "order_total": order_total_price,
        "saved_address": saved_address,
    }
    return render(request, 'payment/Checkout.html', data)
