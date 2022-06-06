from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name' , 'price', 'slug', 'available']
    list_filter = ['available', 'create', 'update']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug':('name',)}
