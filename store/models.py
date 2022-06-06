
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your models here.

# class CustomerInfo(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                 on_delete=models.CASCADE,
#                                 related_name='customer')
#     address = models.CharField(max_length=100)
#     phone = models.IntegerField()
#     city = models.CharField(max_length=50)
#     country = models.CharField(max_length=50)

class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,
                                 decimal_places=3)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, db_index=True)
    available = models.BooleanField(default=True)

    objects = models.Manager()
    is_available = AvailableManager()

    class Meta:
        ordering = ('name',)
        index_together = (('id','slug'),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwags):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwags)
        
    def get_absolute_url(self):
        return reverse(
            'store:product_detail',
            args=[
                self.pk,
                self.slug
            ]
        )

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    products = models.ManyToManyField(Product,
                                    related_name='categories',
                                    blank=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'store:products_list_by_category',
            args=[self.slug]
        )

    def __str__(self):
        return self.name

# class Order(models.Model):
#     customer = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                 on_delete=models.CASCADE,
#                                 related_name='orders')
#     total = models.DecimalField(max_digits=10,
#                                 decimal_places=3)
#     create = models.DateTimeField(auto_now_add=True)
#     update = models.DateTimeField(auto_now=True)

# class OrderItem(models.Model):
#     product = models.ForeignKey(Product,
#                                 on_delete=models.CASCADE,
#                                 related_name='order_items')
#     order = models.ForeignKey(Order,
#                             on_delete=models.CASCADE,
#                             related_name='order_items')
#     quantity = models.IntegerField()
#     create = models.DateTimeField(auto_now_add=True)
#     update = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.product.name


# class PaymentInfo(models.Model):
#     PAYMENT_CHOICES = (
#         ('credit', 'Credit'),
#         ('cash', 'Cash')
#     )
#     STATUS = (
#         ('unconfirmed', 'Unconfirmed'),
#         ('confirmed', 'Confirmed'),
#         ('delivering', 'Delivering'),
#         ('delivered', 'Delivered')
#     )
#     order = models.OneToOneField(Order,
#                                 on_delete=models.CASCADE,
#                                 related_name='payment_info')
#     create = models.DateTimeField(auto_now_add=True)
#     update = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=20, 
#                              choices=STATUS,
#                              default='unconfirmed')




