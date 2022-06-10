from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import *
# Create your views here.

def product_list(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.all()
    else:
        products = Product.objects.all()
    context = {'products' : products}
    return render(request, 'store/product_list.html', context)

@login_required
def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'store/product_detail.html',{'product':product})
