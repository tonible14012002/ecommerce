from dataclasses import field
from django import forms
from .models import Order, OrderItem


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'city']