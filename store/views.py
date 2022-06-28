import json
from time import process_time_ns
from unicodedata import category
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from pkg_resources import require
from .models import *
from account.decorator import ajax_required
from django.views.decorators.http import require_http_methods
from cart.form import CartAddProductForm
# Create your views here.

def products_list(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        category_name = category.__str__()
        products = category.products.all()
    else:
        products = Product.objects.all()
        category_name = None

    paginator = Paginator(products, 6)
    page = paginator.page(1)
    products = page.object_list

    context = {'products' : products, 'num_pages': paginator.num_pages, 'category_slug':category_slug, 'category_name':category_name}
    return render(request, 'store/product_list_page.html', context)

@ajax_required
@require_http_methods(['GET'])
def get_more_products(request, category_slug=None):

    if category_slug:
        category = Category.objects.get(slug = category_slug)
        products = category.products.all()
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 6)
    page = request.GET.get('page')

    try:
        products = paginator.page(page).object_list
    except (PageNotAnInteger, EmptyPage):
        return HttpResponse('')
    return render(request, 'store/show_products.html', {'products':products})

def product_detail(request, pk, product_slug=None):
    product = get_object_or_404(Product, pk=pk)
    form = CartAddProductForm()
    return render(request, 'store/product_detail.html',{'product':product, 'form':form})


