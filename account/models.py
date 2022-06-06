from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


def get_name(self):
    name = ''
    if self.first_name:
        name = self.first_name
    if self.last_name:
        name += ' ' + self.last_name.strip()
    if name:
        return name
    return self.username

get_user_model().add_to_class('get_name', get_name)

# Create your models here.
class CustomerInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='customer_info')
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.get_name() + " info"
    
    class Meta:
        ordering = ['update', 'create']