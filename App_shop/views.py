from django.shortcuts import render
# import view
from django.views.generic import ListView, DetailView
# import models
from .models import Product

# login required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class Home(ListView):
    model = Product
    template_name = 'App_shop/home.html'


class Single_product_Detail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'App_shop/product_detail.html'
