# -*- coding: utf-8 -*-

import json
from leon.apps.base import BaseView, BaseParamsValidatorMixin


class SearchParamsValidatorMixin(BaseParamsValidatorMixin):

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
    def _empty_validator(value, default):
        return value or default


class SearchBaseView(BaseView):

    """ Class Base for all Basket Class Views
        When request is received, then
    """

    pass
