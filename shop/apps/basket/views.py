# coding: utf-8


from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse
from django.contrib.contenttypes.models import ContentType
import json

from .cart import Cart
from catalog.models import PrintType
from .base import BasketBaseView, BasketParamsValidatorMixin


class BasketList(BasketBaseView, BasketParamsValidatorMixin):

    """ Basket List View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. AJAX - if ajax is True, we have response
        html part, that insert in DOM structure in client
        side. If we have True, we response all html
        document with base template.
        2. ITEM_S - list of dicts of items with params
        (
            id: id of product/subproduct,
            count: count of product,
            print_type_id: id of print_type
        )

        ALL PARAMS put in params_storage after validate
    """

    BASKET_MODEL = None

    request_params_slots = {
        'item_s': [None, []],
    }

    session_params_slots = {
        'cart': [None, None],
    }

    session_save_slots = {
        'cart': 'cart_id'
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'cart': None,
            'total_price': None
        }
        super(BasketList, self).__init__(*args, **kwargs)

    def _set_item_s(self):
        self.item_s = self.params_storage['item_s']

    def _set_basket(self):
        self.basket = self.BASKET_MODEL(self.params_storage['cart'])

    def _cart_update_all(self):

        self.cart.calculate()
        self.total_price = str(abs(self.cart.price))

    def get(self, *args, **kwargs):
        self._set_item_s()
        self._set_cart()
        self._cart_update_all()
        self._save_cookies()
        self._aggregate()

        return self._render()


class BasketMenu(BasketBaseView, BasketParamsValidatorMixin):

    """ Basket Menu View. Receives get params
        and response neither arguments in get
        request params.
        Cart Menu using in corner ia all pages,
        and this is relate with your session. This
        class using onle by ajax.

        GET Params:

        1. ITEM_S - list of dicts of items with params
        (
            id: id of product/subproduct,
            count: count of product,
            print_type_id: id of print_type
        )

        ALL PARAMS put in params_storage after validate
    """

    BASKET_MODEL = None

    request_params_slots = {
        'item_s': [None, []],
    }

    session_params_slots = {
        'basket': [None, None],
    }

    session_save_slots = {
        'basket': 'basket_id'
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'basket': None,
            'total_price': None
        }
        super(BasketMenu, self).__init__(*args, **kwargs)

    def _set_cart(self):
        self.basket = self.BASKET_MODEL(self.params_storage['basket'])
        self.basket_id = self.basket.id

    def _cart_update_all(self):

        self.basket.calculate()
        self.total_price = str(abs(self.basket.price))

    def get(self, *args, **kwargs):
        self._set_basket()
        self._basket_update_all()
        self._save_cookies()
        self._aggregate()

        return self._render()


class BasketCalc(BasketBaseView, BasketParamsValidatorMixin):

    """ Basket List View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. AJAX - if ajax is True, we have response
        html part, that insert in DOM structure in client
        side. If we have True, we response all html
        document with base template.
        2. ITEM_S - list of dicts of items with params
        (
            id: id of product/subproduct,
            count: count of product,
            print_type_id: id of print_type
        )

        ALL PARAMS put in params_storage after validate
    """

    BASKET_MODEL = None

    request_params_slots = {
        'item_s': [None, []],
    }

    session_params_slots = {
        'basket': [None, None],
    }

    session_save_slots = {
        'basket': 'basket_id'
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'item_s': None,
            'total_price': None
        }
        super(BasketCalc, self).__init__(*args, **kwargs)

    def _set_item_s(self):
        self.item_s = self.params_storage['item_s']

    def _set_basket(self):
        self.basket = self.BASKET_MODEL(self.params_storage['basket'])

    def _basket_update_all(self):

        item_pk_s = {}
        for item in self.cart:
            item_pk_s[item.product.pk] = item.product

        for item in self.item_s:
            product_obj = self.PRODUCT_MODEL.get_object_(id=item['pk'])
            self.cart.update(product_obj, item['stock'])
            if item['pk'] in item_pk_s:
                del item_pk_s[item['pk']]

        for item_pk, product in item_pk_s.items():
            self.cart.remove(product)

        self.cart.calculate()
        self.total_price = str(abs(self.cart.price))

    def get(self, *args, **kwargs):
        self._set_item_s()
        self._set_cart()
        self._cart_update_all()
        self._save_cookies()
        self._aggregate()

        return HttpResponse(json.dumps(self.output_context))
