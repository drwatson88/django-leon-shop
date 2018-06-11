# -*- coding: utf-8 -*-


from leon_base.base.views import BaseView, BaseParamsValidatorMixin


class LandingParamsValidatorMixin(BaseParamsValidatorMixin):

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
    def _landing_slug_title_validator(value, default):
        return value


class LandingBaseView(BaseView):

    """ Class Base for all Catalog Class Views
        When request is received, then
    """

    pass

