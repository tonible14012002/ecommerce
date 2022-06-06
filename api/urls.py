from django import views
from django.urls import path
from . import views


app_name = 'api'
urlpatterns = [
    path('', views.ProductsApiView.as_view(), name='store'),
    path('django/', views.getProduct)
]