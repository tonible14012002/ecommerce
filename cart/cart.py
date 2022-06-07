
from re import L
from ecommerce.settings import CART_SESSION_ID
from django.conf import settings

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, product, quantity, quantity_override=False):
        if quantity_override:
            pass