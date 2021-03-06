from decimal import Decimal
from django.conf import settings


from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, product, quantity, update_quantity=False):
        product_pk = str(product.pk)
        if product_pk not in self.cart:
            self.cart[product_pk] = {'quantity': 0, 'price': str(product.price)}
            
        if not update_quantity:
            self.cart[product_pk]['quantity'] += quantity
        else:
            self.cart[product_pk]['quantity'] = quantity
        if self.cart[product_pk]['quantity'] == 0:
            self.remove(product)
        self.save()

    def quantity(self, product):
        product_pk = str(product.pk)
        if product_pk not in self.cart:
            return 0
        else:
            return self.cart[product_pk]['quantity']

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def remove(self, product):
        product_pk = str(product.pk)
        if product_pk in self.cart:
            del self.cart[product_pk]
            self.save()
            
    def __iter__(self):
        # Iterate over items in cart, get products in database.
        product_pks = self.cart.keys()
        products = Product.objects.filter(pk__in = product_pks)
        for product in products:
            self.cart[str(product.pk)]['product'] = product
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price']*item['quantity']
            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def total_price(self):
        return sum(item['quantity']*Decimal(item['price']) for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
        
    