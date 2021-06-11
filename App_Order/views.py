from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# import models
from .models import Card, Order
from App_shop.models import Product

# message
from django.contrib import messages


# Create your views here.

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Card.objects.get_or_create(product=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)  # total order items current user
    if order_qs.exists():
        order = order_qs[0]  # tuple to convert string_or_array
        if order.orderItems.filter(product=item).exists():  # click item ta Order model a ache ki na check korbe
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, 'this item quantity was updated or 1 incorrect !')
            return redirect('App_shop:homepage')
        else:
            order.orderItems.add(order_item[0])  # user already added to Order model . so item added
            messages.info(request, 'This item was added  to your Cart !!!')
            return redirect('App_shop:homepage')
    else:
        order = Order(user=request.user)
        order.save()  # user added to Order Model
        order.orderItems.add(order_item[0])  # add item Oder model
        messages.info(request, 'This item was added  to your Cart !')
        return redirect('App_shop:homepage')


@login_required
def Cart_view(request):
    carts = Card.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        data = {
            "title": 'Cart',
            "carts": carts,
            "order": order,
            # "total_order_items": order.orderItems.count(), # or templatetags user
        }
        return render(request, 'App_order/cart.html', data)
    else:
        messages.warning(request, "You don't have any item in your cart !!")
        return redirect('App_shop:homepage')


@login_required
def remove_from_cart(request, pk, ):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)  # total order items current user
    if order_qs.exists():
        order = order_qs[0]  # tuple to convert string_or_array
        if order.orderItems.filter(product=item).exists():  # click item ta Order model a ache ki na check korbe
            order_item = Card.objects.filter(product=item, user=request.user, purchased=False)[0]
            order.orderItems.remove(order_item)  # order model theke delete hobe
            order_item.delete()  # card model theke delete hobe
            messages.info(request, "This item was remove form your cart.")
            return redirect('App_Order:cart_view')

        else:
            messages.info(request, 'This item was not in your cart.')
            return redirect('App_shop:homepage')
    else:
        messages.info(request, "you don't have an active order")
        return redirect('App_shop:homepage')


@login_required
def cart_quantity_increment(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)  # total order items current user
    if order_qs.exists():
        order = order_qs[0]  # tuple to convert string_or_array
        if order.orderItems.filter(product=item).exists():  # click item ta Order model a ache ki na check korbe
            order_item = Card.objects.filter(product=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated(+) !!")
                return redirect('App_Order:cart_view')
        else:
            messages.info(request, f"{item.name} in not your cart !!")
            return redirect('App_shop:homepage')
    else:
        messages.info(request, "you don't have an active order")
        return redirect('App_shop:homepage')


@login_required
def cart_quantity_decrement(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order_list = order_qs[0]
        if order_list.orderItems.filter(product=item).exists():
            order_item = Card.objects.filter(product=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated(-) !!")
                return redirect('App_Order:cart_view')
            else:
                order_list.orderItems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name}  has been remove form cart  !!")
                return redirect('App_Order:cart_view')
        else:
            messages.warning(request, f"{item.name} in not your cart !!")
            return redirect('App_shop:homepage')
    else:
        messages.info(request, "you don't have an active order")
        return redirect('App_shop:homepage')
