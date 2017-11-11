# coding: utf-8


from leon.apps.base import BaseContextProcessor
from .base import BasketParamsValidatorMixin


class ShopBasketMenuContextProcessor(BaseContextProcessor, BasketParamsValidatorMixin):

    """
    Class for block context processor menu
    """

    kwargs_params_slots = {
    }

    request_params_slots = {
        'basket': [None, {}]
    }

    PRODUCT_MODEL = None
    BASKET_CONTAINER = None

    def _set_basket(self, request):
        self.basket = self.BASKET_CONTAINER(request.session, request.user)

    def _update_all(self):
        item_s = self.params_storage['basket'].get('item_s', [])
        if not item_s:
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

    def __call__(self, request):
        self.output_context = {
            'basket': None
        }
        self._init(request)
        self._set_basket(request)
        self._update_all()
        self._aggregate()
        return self.output_context
