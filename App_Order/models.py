from django.db import models
from django.conf import settings
from App_shop.models import Product


# Create your models here.

class Card(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='card')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.product}'

    def get_total_price(self):
        total = self.quantity * self.product.price
        float_total = format(total, '0.2f')
        return float_total


class Order(models.Model):
    orderItems = models.ManyToManyField(Card)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)

    def get_totals(self):
        total = 0
        for order_items in self.orderItems.all():
            total += float(order_items.get_total_price())
        return total
