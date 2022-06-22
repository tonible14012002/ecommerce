from django import views
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_pk>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_pk>/', views.cart_remove, name='cart_remove'),
    path('detail/', views.cart_detail, name='cart_detail')
]