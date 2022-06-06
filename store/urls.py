from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('<slug:category_slug>', views.ProductList, name='products_list_by_category'),
    path('', views.ProductList, name='products_list'),
    path('<int:id>/<slug:product_slug>', views.product_detail, name='product_detail')
]