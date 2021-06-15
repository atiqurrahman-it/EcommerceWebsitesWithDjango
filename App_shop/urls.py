from django.urls import path
from . import views

app_name = 'App_shop'
urlpatterns = [
    path('', views.Home.as_view(), name='homepage'),
    path('product/<pk>', views.Single_product_Detail.as_view(), name='single_product'),

]
