from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from .forms import BillingForm
from App_Order.models import Order
from .models import BillingAddress
from user_login.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# payment for import
import requests
import socket
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal

# csr validation not check
from django.views.decorators.csrf import csrf_exempt


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


def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.info(request, f"please complete shipping Address  !")
        return redirect("App_payment:checkout")
    if not request.user.profile.profile_is_fully_filled():
        messages.info(request, f"please complete profile Details !")
        return redirect("user_login:edit_profile")
    # upper code just formality and check fill up  shipping address and profile
    # we meed shipping Address and profile details so we check this models fill up

    # payment for email import id and key
    store_id = 'ecomm60c859144dc58'
    api_key = 'ecomm60c859144dc58@ssl'
    my_payment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=api_key)
    # request.build_absolute_uri() current url call kore niye ase
    status_url = request.build_absolute_uri(reverse("App_payment:p_complete"))
    # p_complete call kore niye asbe
    my_payment.set_urls(success_url=status_url, fail_url=status_url,
                        cancel_url=status_url, ipn_url=status_url)
    # Product Order details
    order_details = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_details[0].orderItems.all()
    total_tk = order_details[0].get_totals()
    number_of_order_items = order_details[0].orderItems.count()
    my_payment.set_product_integration(total_amount=Decimal(total_tk), currency='BDT', product_category='Mixed',
                                       product_name=order_items, num_of_item=number_of_order_items,
                                       shipping_method='Courier',
                                       product_profile='None')
    # current payment customer details
    # current user information
    current_user = request.user
    user_info = Profile.objects.filter(user=current_user)[0]
    my_payment.set_customer_info(name=user_info.full_name, email=current_user.email, address1=user_info.address_1,
                                 address2=user_info.address_1, city=user_info.city, postcode=user_info.zipcode,
                                 country=user_info.country,
                                 phone=user_info.phone)

    # shipping Address
    # saved_address = BillingAddress.objects.get_or_create(user=request.user)
    my_payment.set_shipping_info(shipping_to=user_info.full_name, address=saved_address.address,
                                 city=saved_address.city, postcode=saved_address.zipcode,
                                 country=saved_address.country)

    response_data = my_payment.init_payment()
    return redirect(response_data['GatewayPageURL'])

    # data = {
    #     "title": 'payment',
    # }
    # return render(request, 'payment/payment.html', data)


@csrf_exempt
def CompletePayment(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']

        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request, f"Your payment completed successfully ! please will be redirected after 5 second !")
        elif status == 'FAILED':
            messages.warning(request, f"Your payment ! please Try Again ! please will be redirected after 5 second !")
        elif status == 'CANCELLED':
            messages.warning(request, f"Your payment has been cancel . please Try Again ! please will be redirected after 5 second !")

    # print(payment_data)
    data = {
        "title": 'complete payment'
    }
    return render(request, 'payment/p_complete.html', data)
