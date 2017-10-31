# coding: utf-8


from leon.base import BaseContextProcessor
from .base import BasketParamsValidatorMixin


class BasketMenuContextProcessor(BaseContextProcessor, BasketParamsValidatorMixin):

    """
    Class for block context processor menu
    """

    kwargs_params_slots = {
    }

    CATEGORY_SITE_MODEL = None

    def _create_data(self, request):
        self.basket = self.BASKET_MODEL.get_current(request)

    def __call__(self, request):
        self.main_menu = {}
        self.output_context = {
            'basket': None
        }
        self._init(request)
        self._create_data(request)
        self._aggregate()
        return self.output_context
