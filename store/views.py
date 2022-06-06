from operator import ipow
from django.shortcuts import render
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
    
