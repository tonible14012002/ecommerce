from turtle import update
from django import forms

PRODUCT_QUANTITY_CHOICES = ((i, str(i)) for i in range(1,13))

class CartAddProductForm(forms.Form):
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    quantity = forms.TypedChoiceField(coerce=int, choices=PRODUCT_QUANTITY_CHOICES, initial=1)
    
    def __init__(self, *args, **kwargs):
        stock = kwargs.pop('stock')
        cart_quantity = kwargs.pop('cart_quantity')
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        self.stock = stock
        self.cart_quantity = cart_quantity
        self.fields['quantity'].choices = ((i, str(i)) for i in range(0, self.stock+2))

    
    def clean_quantity(self):
        q = self.cleaned_data['quantity']
        update_quantity = self.cleaned_data['update']
        if update_quantity and q > self.stock:
            raise forms.ValidationError(f'There are only {self.stock} left in stock')
        if not update_quantity and q > self.stock - self.cart_quantity:
            raise forms.ValidationError(f'There are only {self.stock - self.cart_quantity} left in stock')
        return q