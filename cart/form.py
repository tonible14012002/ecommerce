from email.policy import default
from django import forms

#quantity 0-20
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,21)] 

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(coerce=int, choices=PRODUCT_QUANTITY_CHOICES)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
