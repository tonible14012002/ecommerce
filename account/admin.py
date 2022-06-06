from django.contrib import admin
from .models import CustomerInfo
# Register your models here.
@admin.register(CustomerInfo)
class CustomerInfoAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone', 'city', 'country', 'create', 'update']
    