from multiprocessing.reduction import steal_handle
from django.db import models
from django.forms import SelectDateWidget
from store.models import Product
# Create your models here.
class Order(models.Model):

    STATUS_CHOICE = (
        ('UNCONFIRMED','Unconfirmed'),
        ('CONFIRMED', 'Confirmed'),
        ('DELIVERING', 'Delivering'),
        ('DELIVERED', 'Delivered')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICE, default=STATUS_CHOICE[0][1], max_length=50)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=3)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity