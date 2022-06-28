
from django import forms
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render
from store.models import Product
from .form import CartAddProductForm
from .cart import Cart
# Create your views here.

from account.decorator import ajax_required

@ajax_required
@require_http_methods(['POST'])
def cart_add(request, product_pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_pk)
    form = CartAddProductForm(
        request.POST,
        stock=product.stock,
        cart_quantity=cart.quantity(product)
    )
    if form.is_valid():
        cart.add(
            product=product,
            quantity=form.cleaned_data['quantity'],
            update_quantity=form.cleaned_data['update']
        )
        return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'error', 'errors': form.errors})

@ajax_required
def cart_remove(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    cart = Cart(request)
    cart.remove(product)
    return JsonResponse({'status':'ok'})

@ajax_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html',{'cart': cart})

