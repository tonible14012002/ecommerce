from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def checkout(request):
    return HttpResponse("checkout page")