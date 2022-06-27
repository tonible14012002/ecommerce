from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from cart.cart import Cart
# Create your views here.

def checkout(request):
    context = {}
    cart = Cart(request)
    return HttpResponse('fixing')

