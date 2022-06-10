from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views


app_name = 'account'
urlpatterns = [
    path('login/', views.login_page, name='login') ,
    path('login_user/',views.login_user, name='login_user'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('account:login')), name='logout'),
    path('password-change/', views.password_change_form,name='password_change'),
    path('password-change/request', views.password_change_request, name='password_change_request'),
    path('password-reset/', views.password_reset_form, name='password_reset'),
    path('password-reset/request', views.password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/<uidb64>/<token>', views.password_reset_confirm_form, name='password_reset_confirm'),
    path('password-reset/confirm/request/<uidb64>/<token>', views.password_reset_confirm_request, name='password_reset_confirm_request'),
    path('register/', views.register_page, name='register'),
    path('register/request', views.register_request, name='register_request'),
    path('activate/<uidb64>/<token>', views.account_activation, name='account_activation'),
    path('activate/', views.account_activation_request, name='account_activation_request'),
    path('add-info/', views.add_info, name='add_info')
]