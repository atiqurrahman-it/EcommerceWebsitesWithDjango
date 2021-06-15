from django.urls import path
from . import views

app_name = 'App_payment'
urlpatterns = [
    path('checkout/', views.Checkout, name='checkout'),
    path('py/', views.payment, name='payment'),
    path('status/', views.CompletePayment, name='p_complete'),
    path('purchase/<val_id>/<tran_id>/', views.purchase, name='purchase'),
    path('order/', views.order_views, name='pay_order'),

]
