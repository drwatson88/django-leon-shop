# coding: utf-8


from leon_base.base.context_processors import BaseContextProcessor
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

    def __call__(self, request):
        self.output_context = {
            'basket': None
        }
        self._init(request)
        self._set_basket(request)
        self._aggregate()
        return self.output_context
