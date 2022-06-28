
from secrets import choice
from statistics import quantiles
from django import forms

PRODUCT_QUANTITY_CHOICES = ((i, str(i)) for i in range(21))

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(coerce=int, choices=PRODUCT_QUANTITY_CHOICES, initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)

