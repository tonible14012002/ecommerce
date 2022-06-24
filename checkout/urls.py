from tabnanny import check
from django.http import HttpResponse
from django.urls import path

app_name = 'checkout'

def checkout(request):
    return HttpResponse('asdas')

urlpatterns = [
    path('', checkout, name='checkout')
]