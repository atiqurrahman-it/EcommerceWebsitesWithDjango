from django.urls import path
from .import views
app_name = 'App_Order'
urlpatterns = [
     path('cart/<pk>/',views.add_to_cart,name='add_cart'),
     path('cart_view/',views.Cart_view,name='cart_view'),
     path('remove_cart/<pk>/',views.remove_from_cart,name='remove_cart'),
     path('remove_cart/<pk>/',views.remove_from_cart,name='remove_cart'),
     path('increment/<pk>/',views.cart_quantity_increment,name='increment'),
     path('decrement/<pk>/',views.cart_quantity_decrement,name='decrement'),

]