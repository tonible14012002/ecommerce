from email.policy import default
from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(max_value=21, min_value=1, initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
