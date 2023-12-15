# https://dev.to/nick_langat/building-a-shopping-cart-using-django-rest-framework-54i0

from decimal import Decimal

from django.conf import settings

# from .serializers import ProductSerializer
from .models import Byte


class Cart:
    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, byte, quantity=1, overide_quantity=False):
        """
        Add item to the cart or update its quantity
        """

        byte_id = str(byte["id"])
        if byte_id not in self.cart:
            self.cart[byte_id] = {
                "quantity": 0,
                "price": str(byte["price"])
            }
        if overide_quantity:
            self.cart[byte_id]["quantity"] = quantity
        else:
            self.cart[byte_id]["quantity"] += quantity
        self.save()

    def remove(self, byte):
        """
        Remove a item from the cart
        """
        byte_id = str(byte["id"])

        if byte_id in self.cart:
            del self.cart[byte_id]
            self.save()

    def __iter__(self):
        """
        Loop through cart items and fetch the items from the database
        """
        byte_ids = self.cart.keys()
        bytes = Byte.objects.filter(id__in=byte_ids)
        cart = self.cart.copy()
        # for byte in bytes:
        #     cart[str(byte.id)]["byte"] = ProductSerializer(byte).data
        for item in cart.values():
            item["price"] = Decimal(item["price"]) 
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()