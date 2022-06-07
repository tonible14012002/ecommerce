from django.db import models
from django.conf import settings
from store.models import Product

# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='orders')
    total = models.DecimalField(max_digits=10,
                                decimal_places=3)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='order_items')
    order = models.ForeignKey(Order,
                            on_delete=models.CASCADE,
                            related_name='order_items')
    quantity = models.IntegerField(default=1)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name