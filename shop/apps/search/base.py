# -*- coding: utf-8 -*-

import json
from leon.apps.base import BaseView, BaseParamsValidatorMixin


class SearchParamsValidatorMixin(BaseParamsValidatorMixin):

    """ Mixin with validators for validate
        request parameters.
    """

    @staticmethod
    def _query_validator(value, default):
        return value or default


class SearchBaseView(BaseView):

    """ Class Base for all Basket Class Views
        When request is received, then
    """

    pass
