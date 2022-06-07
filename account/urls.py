from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views


app_name = 'account'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login') ,
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('account:login')), name='logout'),
    path('password-change/', views.password_change_form,name='password_change_form'),
    path('password-reset/', views.password_reset_form, name='password_reset_form'),
    path('register/', views.register_page, name='register'),
    path('add-info/', views.add_info, name='add_info')
]