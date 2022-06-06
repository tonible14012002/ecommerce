from django import views
from django.urls import path
from . import views


app_name = 'api'
urlpatterns = [
    path('', views.ProductsApiView.as_view(), name='products_list'),
    path('<slug:category_slug>/', views.product_list, name='products_list_by_category')
    
]