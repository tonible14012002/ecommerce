from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('products/<slug:category_slug>/', views.products_list, name='products_list_by_category'),
    path('products/', views.products_list, name='products_list'),
    path('get-products/<slug:category_slug>/', views.get_more_products, name='get_more_products_by_category'),
    path('get-products/', views.get_more_products, name='get_more_products'),
    path('<int:id>/<slug:product_slug>/', views.product_detail, name='product_detail')
]