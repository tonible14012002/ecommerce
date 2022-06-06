
from rest_framework import serializers
from store.models import *
from account.models import CustomerInfo
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description', 'slug', 'get_absolute_url']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name' , 'categories' , 'description', 'price', 'update', 'get_absolute_url']
    categories = CategorySerializer(many=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = ['user', 'address', 'phone', 'city', 'country']
    