# coding: utf-8


import datetime
from . import models


class ItemAlreadyExists(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class DiscountMixin(object):

    pass


class ShopBasketContainer(object):

    """ Class for operate basket in session.
        Using request.session dict, where
        find BASKET_ID and if basket object
        not expired and find, return it,
        else, create new object cart.
    """

    BASKET_MODEL = None
    BASKET_ITEM_MODEL = None

    def __init__(self, session, user):
        basket = self.BASKET_MODEL
        if user.is_authenticated():
            basket = basket.objects.filter(user=user, checked_out=False)
        else:
            basket = basket.objects.filter(session_id=session.session_key, checked_out=False)
        basket = basket.first()

        if basket:
            self.basket = basket
        else:
            self.basket = self._create(session, user)

    def __iter__(self):
        for item in self.basket.item_set.all():
            yield item

    def _create(self, session, user):
        data = {'creation_date': datetime.datetime.now()}
        if user.is_authenticated():
            data.update({'user': user})

        data.update({'session_id': session.session_key})
        basket = self.BASKET_MODEL(**data)
        basket.save()
        return basket

    @staticmethod
    def get_image(product):
        return product.main_image()

    def add_item(self, product, quantity=1):
        item = self.BASKET_ITEM_MODEL.objects.filter(basket=self.basket,
                                                     product=product).first()
        if item:
            item.quantity += int(quantity)
        else:
            item = self.BASKET_ITEM_MODEL(basket=self.basket,
                                          product=product,
                                          quantity=quantity)
        item.save()

    def remove(self, product):
        item = self.BASKET_ITEM_MODEL.objects.filter(basket=self.basket, product=product).first()
        if item:
            item.delete()
        else:
            raise ItemDoesNotExist

    def update(self, product, quantity=1):
        item = self.BASKET_ITEM_MODEL.objects.filter(basket=self.basket, product=product).first()
        if not item:
            item = self.BASKET_ITEM_MODEL(basket=self.basket,
                                          product=product,
                                          quantity=quantity)
        item.quantity = quantity
        item.save()

    def calculate(self):
        total_price = 0
        for item in self.basket.item_set.all():
            item.unit_price = item.product.price
            item.item_price = item.unit_price * item.quantity
            item.save()
            total_price += item.item_price
        self.price = total_price

    def clear(self):
        for item in self.basket.item_set.all():
            item.delete()

    def get_quantity(self, product):
        item_s = self.ITEM_MODEL.objects.filter(cart=self.id,
                                                product=product).all()
        if item_s:
            item = item_s[0]
            return item.quantity
        else:
            raise ItemDoesNotExist

    def checkout_cart(self):
        self.basket.checked_out = True
        self.basket.save()
        return True

    def total(self):
        total = 0
        for item in self.basket.item.all():
            total += item.total()
        return total

    def count(self):
        total = 0
        for item in self.basket.item.all():
            total += item.quantity
        return total

    def item_s(self):
        return self.basket.item.all()

    def has_items(self):
        return self.item_count() > 0
