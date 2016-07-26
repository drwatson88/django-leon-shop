# -*- coding: utf-8 -*-

import json
from leon.base import BaseView, ParamsValidatorMixin


class CatalogParamsValidatorMixin(ParamsValidatorMixin):

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
    def _grid_validator(value, default):
        if value == 'grid':
            return 1
        elif value == 'list':
            return 0
        else:
            return 1

    @staticmethod
    def _grid_cnt_validator(value, default):
        return default

    @staticmethod
    def _order_validator(value, default):
        return default

    @staticmethod
    def _page_no_validator(value, default):
        return default

    @staticmethod
    def _page_size_validator(value, default):
        return default

    @staticmethod
    def _brand_id_s_validator(value, default):
        try:
            return json.loads(value)
        except BaseException as exc:
            return default

    @staticmethod
    def _product_stock_validator(value, default):
        return default


class CatalogBaseView(BaseView):

    """ Class Base for all Catalog Class Views
        When request is received, then
    """

    pass
