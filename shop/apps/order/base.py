# -*- coding: utf-8 -*-


from formtools.wizard.views import NamedUrlSessionWizardView
from leon.apps.base import BaseView, BaseParamsValidatorMixin


class OrderParamsValidatorMixin(BaseParamsValidatorMixin):

    """ Mixin with validators for validate
        request parameters.
    """

    @staticmethod
    def _ajax_validator(value, default):
        try:
            return int(value)
        except BaseException as exc:
            return default


class OrderBaseWizardView(NamedUrlSessionWizardView, BaseView):

    """ Class Base for all Catalog Class Views
        When request is received, then
    """

    @classmethod
    def as_view(cls, *args, **kwargs):
        cls._install_validate_s()
        return super(OrderBaseWizardView, cls).as_view(*args, **kwargs)

    def done(self, form_list, **kwargs):
        pass
