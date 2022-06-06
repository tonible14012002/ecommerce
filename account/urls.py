from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('add-info/', views.add_info, name='add_info')
]