# -*- coding: utf-8 -*-

import json
from leon.base import BaseView, ParamsValidatorMixin


class BasketParamsValidatorMixin(ParamsValidatorMixin):

    """ Mixin with validators for validate
        request parameters.
    """

    @staticmethod
    def _ajax_validator(value, default):
        try:
            return int(value)
        except BaseException as exc:
            return default

    @staticmethod
    def _item_s_validator(value, default):
        try:
            return json.loads(value)
        except BaseException as exc:
            return default

    @staticmethod
    def _cart_validator(value, default):
        try:
            return value
        except BaseException as exc:
            return default


class BasketBaseView(BaseView):

    """ Class Base for all Basket Class Views
        When request is received, then
    """

    pass
