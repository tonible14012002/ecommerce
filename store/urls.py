from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('all-collections/<slug:category_slug>/', views.product_list_page, name='products_list_by_category'),
    path('all-collections/', views.product_list_page, name='products_list'),
    path('get-products', views.products_list, name='get_product_list'),
    path('get-products/<slug:category_slug>/', views.products_list, name='get_product_list'),    
    
    path('more_products/<slug:category_slug>/', views.more_products, name='more_products_by_category'),
    path('more_products/', views.more_products, name='more_products'),

    path('<int:pk>/<slug:product_slug>/', views.product_detail, name='product_detail')
]