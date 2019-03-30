# thanks to https://blog.muva.tech/developing-shopping-cart-class-shop-products-django-2-0-python-3-6/

from decimal import Decimal
from django.conf import settings

from pyrebase import pyrebase



config = {
    'apiKey': "AIzaSyA-W5UF_rvGjzUuSxPwNOQb0wO8q0cDl5A",
    'authDomain': "muja-mall.firebaseapp.com",
    'databaseURL':  "https://muja-mall.firebaseio.com",
    'projectId': "muja-mall",
    'storageBucket': "muja-mall.appspot.com",
    'messagingSenderId': "424974719406"


}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.key())
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.val()['price'])}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.key())
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        pro = db.child("products").get()
        products = []
        pp = None
        for p in pro.each():
            
            
            if p.key() in product_ids:
                pp = p.val()
                pp['key'] = p.key()
                products.append(pp)

        
        for product in products:
            self.cart[str(product['key'])]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True