from django.urls import path
from . import views
app_name = 'checkout'
urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('order_detail', views.order_detail, name='order_detail')
]