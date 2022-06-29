from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from account.decorator import ajax_required
from django.views.decorators.http import require_http_methods
from cart.cart import Cart
from .form import CreateOrderForm
# Create your views here.

def checkout(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'checkout/checkout_page.html', context)

def order_detail(request):
    form = CreateOrderForm()
    return render(request,'checkout/create_order_form.html',{'form': form})