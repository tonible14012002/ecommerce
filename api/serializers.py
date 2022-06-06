from dataclasses import field
from pyexpat import model
from statistics import mode
from tkinter.tix import Tree
from unicodedata import name
from rest_framework import serializers
from store.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name' , 'categories' , 'description', 'price', 'update']
    categories = CategorySerializer(many=True)

