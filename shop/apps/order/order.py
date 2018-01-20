# coding: utf-8


import datetime
from . import models


class ItemAlreadyExists(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class DiscountMixin(object):

    pass


class ShopOrderContainer(object):

    """ Class for operate order in session.
        Using request.session dict, where
        find ORDER_ID and if order object
        not expired and find, return it,
        else, create new object cart.
    """

    ORDER_MODEL = None
    ORDER_ITEM_MODEL = None

    def __init__(self, session, user):
        order = self.ORDER_MODEL
        if user.is_authenticated():
            order = order.objects.filter(user=user, checked_out=False)
        else:
            order = order.objects.filter(session_id=session.session_key, checked_out=False)
        order = order.first()

        if order:
            self.order = order
        else:
            self.order = self._create(session, user)

    def __iter__(self):
        for item in self.order.item_set.all():
            yield item

    def _create(self, session, user):
        data = {'creation_date': datetime.datetime.now()}
        if user.is_authenticated():
            data.update({'user': user})

        data.update({'session_id': session.session_key})
        order = self.ORDER_MODEL(**data)
        order.save()
        return order

    @staticmethod
    def get_image(product):
        return product.main_image()

    def add_item(self, product, quantity=1):
        item = self.ORDER_ITEM_MODEL.objects.filter(order=self.order,
                                                     product=product).first()
        if item:
            item.quantity += int(quantity)
        else:
            item = self.ORDER_ITEM_MODEL(order=self.order,
                                          product=product,
                                          quantity=quantity)
        item.save()

    def remove(self, product):
        item = self.ORDER_ITEM_MODEL.objects.filter(order=self.order, product=product).first()
        if item:
            item.delete()
        else:
            raise ItemDoesNotExist

    def update(self, product, quantity=1):
        item = self.ORDER_ITEM_MODEL.objects.filter(order=self.order, product=product).first()
        if not item:
            item = self.ORDER_ITEM_MODEL(order=self.order,
                                          product=product,
                                          quantity=quantity)
        item.quantity = quantity
        item.save()

    def update_fields(self, **fields):
        for k, v in fields.items():
            setattr(self.order, k, v)
        self.order.save()

    def update_items(self, pitems):
        for k, v in pitems.items():
            self.update(k, v)

    def calculate(self):
        total_price = 0
        for item in self.order.item_set.all():
            item.unit_price = item.product.price
            item.item_price = item.unit_price * item.quantity
            item.save()
            total_price += item.item_price
        self.price = total_price

    def clear(self):
        for item in self.order.item_set.all():
            item.delete()

    def get_quantity(self, product):
        item_s = self.ITEM_MODEL.objects.filter(cart=self.id,
                                                product=product).all()
        if item_s:
            item = item_s[0]
            return item.quantity
        else:
            raise ItemDoesNotExist

    def checkout(self):
        self.order.checked_out = True
        self.order.save()
        return True

    def total(self):
        total = 0
        for item in self.order.item.all():
            total += item.total()
        return total

    def count(self):
        total = 0
        for item in self.order.item.all():
            total += item.quantity
        return total

    def item_s(self):
        return self.order.item.all()

    def has_items(self):
        return self.item_count() > 0
