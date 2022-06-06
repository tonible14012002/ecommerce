from django.shortcuts import render
from .serializers import ProductSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import *

from api import serializers
# Create your views here.


class ProductsApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(['GET'])
def product_list(request, category_slug=None):
    if category_slug:
        products = Product.is_available.filter(
            categories__slug=category_slug
            )
        if not products.count():
            products = None
    else:
        products = Product.is_available.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)