from math import prod
from operator import ipow
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import *
# Create your views here.

def home(request):
    return HttpResponse('Home page for store')

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    queryset: Product.objects.all()

def ProductList(request, category_slug=None):
    if category_slug:
        products = Product.is_available.filter(categories__slug=category_slug)
        if not products.count():
            products = []
    else:
        products = Product.is_available.all()
    context = {'products' : products}
    return render(request, 'store/product_list.html', context)

def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'store/product_detail.html',{'product':product})