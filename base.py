# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404, HttpResponse
from django.views.generic import View
from django.utils.decorators import classonlymethod


class ParamsValidatorMixin(object):

    @staticmethod
    def _ajax_validator(value, default):
        return default

    @staticmethod
    def _grid_validator(value, default):
        return default

    @staticmethod
    def _grid_cnt_validator(value, default):
        return default

    @staticmethod
    def _order_by_validator(value, default):
        return default

    @staticmethod
    def _page_no_validator(value, default):
        return default

    @staticmethod
    def _brand_id_s_validator(value, default):
        return default


class CatalogBaseView(View):

    """ Class Base for all Catalog Class Views
        When request is received, then
    """

    params_slots = {}
    params_storage = {}

    @classmethod
    def _install_validate_s(cls):
        for param in cls.params_slots:
            cls.params_slots[param][0] = getattr(cls, '_{param}_validator'.format(param=param))

    @classmethod
    def as_view(cls, **initkwargs):
        cls._install_validate_s()
        return super(CatalogBaseView, cls).as_view(**initkwargs)

    def dispatch(self, request, *args, **kwargs):

        """ Dispatch redetermine for route in validate
            for every method and every param

            :param request Request http
            :type request object

        """

        method = getattr(request, 'method')
        method_params = getattr(request, method.upper())
        validators = getattr(self, 'params_slots')
        self.params_storage = {}
        for k, v in validators.items():
            validator = v[0]
            default = v[1]
            self.params_storage[k] = validator(method_params.get(k), default)
        return super(CatalogBaseView, self).dispatch(request, *args, **kwargs)

