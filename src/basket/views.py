# coding: utf-8

import json
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse

from .base import BasketBaseView, BasketParamsValidatorMixin


class ShopBasketView(BasketBaseView, BasketParamsValidatorMixin):

    """ Basket Inside View. Receives get params
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

    PRODUCT_MODEL = None
    BASKET_CONTAINER = None

    request_params_slots = {
        'empty': [None, False],
        'basket': [None, {}]
    }

    session_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'basket': None
        }
        super(ShopBasketView, self).__init__(*args, **kwargs)

    def _set_basket(self):
        self.basket = self.BASKET_CONTAINER(self.request.session, self.request.user)

    def _update_all(self):
        item_s = self.params_storage['basket'].get('item_s', [])
        if not self.popup or self.params_storage['empty']:
            return
        for item in item_s:
            product = self.PRODUCT_MODEL.objects.get(pk=item['pk'])
            quantity = item['quantity']
            self.basket.update(product, quantity)

        remove_item_s = set(item.product.pk for item in self.basket.item_s()) - \
                        set(item['pk'] for item in item_s)
        for product_pk in remove_item_s:
            product = self.PRODUCT_MODEL.objects.get(pk=product_pk)
            self.basket.remove(product)

    def get(self, *args, **kwargs):
        self._set_basket()
        self._update_all()
        self._aggregate()
        return self._render()


class ShopBasketCalcView(BasketBaseView, BasketParamsValidatorMixin):

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
        super(ShopBasketCalcView, self).__init__(*args, **kwargs)

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
