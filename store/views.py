from asyncio import constants
import json
import re
from time import process_time_ns, sleep
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from pkg_resources import require
from cart.cart import Cart

from cart.views import cart_add
from .models import *
from account.decorator import ajax_required
from django.views.decorators.http import require_http_methods
from cart.form import CartAddProductForm

from django.template.loader import render_to_string

from django.db.models import Q

# Create your views here.
PRODUCTS_PER_PAGE = 4

def product_list_page(request,category_slug = None):
    
    category_name = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        category_name = category.name

    context = {'category_slug':category_slug, 'category_name':category_name}
    return render(request, 'store/product_list_page.html', context)


@ajax_required
def products_list(request, category_slug=None):

    sleep(1)
        
    if request.method == 'GET':    
        q = request.GET.get('q')
    if q is None:
        q = ''
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.filter(
            Q(name__icontains=q) |
            Q(categories__name__icontains=q)
        ).distinct()
    else:
        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(categories__name__icontains=q)
        ).distinct()

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    page_obj = paginator.page(1)
    products = page_obj.object_list

    html = render_to_string('store/components/product_list.html', {'products' : products})

    page_info = json.dumps({
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'has_other_pages': page_obj.has_other_pages(),
        'current_page': page_obj.number,
        'q':q
    })
    
    script = render_to_string('store/components/handle_paginator.js', {'page_info': page_info, 'category_slug': category_slug})
    
    return JsonResponse({'html': html, 'script':script})

@ajax_required
def more_products(request, category_slug=None):
    sleep(1)
    
    if request.method == 'GET':    
        q = request.GET.get('q')
    if q is None:
        q = ''

    page = request.GET.get('page')
    print(page)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.filter(
            Q(name__icontains=q) |
            Q(categories__name__icontains=q)
        ).distinct()
    else:
        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(categories__name__icontains=q)
        ).distinct()

    paginator = Paginator(products, PRODUCTS_PER_PAGE)
    try:
        page_obj = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    products = page_obj.object_list
    html = render_to_string('store/components/show_products.html', {'products': products})

    page_info = {
        'category_slug': category_slug,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'has_other_pages': page_obj.has_other_pages(),
        'current_page': page_obj.number,
        'q':q
    }

    return JsonResponse({'html': html, 'page_info': page_info})

def product_detail(request, pk, product_slug=None):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart(request)
    form = CartAddProductForm(stock=product.stock,cart_quantity=cart.quantity(product))
    return render(request, 'store/product_detail.html',{'product':product, 'form':form})


