# coding: utf-8

import json
from django.shortcuts import HttpResponse
from django.contrib.sessions.backends.db import SessionStore
from .base import OrderBaseWizardView, OrderParamsValidatorMixin, OrderBaseView


class ShopOrderView(OrderBaseWizardView, OrderParamsValidatorMixin):
    """ Category List View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. AJAX - if ajax is True, we have response
        html part, that insert in DOM structure in client
        side. If we have True, we response all html
        document with base template.

        ALL PARAMS put in params_storage after validate
    """

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            '': None
        }
        super(ShopOrderView, self).__init__(*args, **kwargs)

    def done(self, form_list, **kwargs):
        pass

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._aggregate()
        return self._render()


class ShopOrderWizardView(OrderBaseWizardView):

    """

    """

    template_name = None

    form_list = [
        ('service', None),
        ('shortcontact', None),
        ('couriercontact', None),
        ('fullcontact', None),
        ('payment', None),
        ('confirm', None),
    ]

    def context_service_init(self):
        pass

    def initial_contact_init(self):
        pass

    def context_payment_init(self):
        pass

    def context_confirm_init(self):
        pass

    def get_form_initial(self, step):
        pass

    def get_context_data(self, form, **kwargs):
        return super(ShopOrderWizardView, self).get_context_data(form=form, **kwargs)

    def render(self, form=None, **kwargs):
        form = form or self.get_form()
        context = self.get_context_data(form=form, **kwargs)
        self.output_context.update(context)
        return self._render()

    def done(self, form_list, **kwargs):
        pass


class ShopOrderUserCityView(OrderBaseView, OrderParamsValidatorMixin):

    """ Product User City View.
    """

    CITY_MODEL = None

    request_params_slots = {
        'city_id': [None, 0]
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            '': None
        }
        super(ShopOrderUserCityView, self).__init__(*args, **kwargs)

    def _session_init(self):
        self.session_store = self.request.session

    def _city_init(self):
        city_id = self.params_storage['city_id']
        self.session_store['city_id'] = city_id if city_id else None

    def get(self, *args, **kwargs):
        self._session_init()
        self._city_init()
        self._aggregate()
        return HttpResponse(json.dumps(self.output_context))
