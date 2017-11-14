# coding: utf-8


from formtools.wizard.views import NamedUrlSessionWizardView
from .base import OrderBaseView, OrderParamsValidatorMixin


class ShopOrderView(OrderBaseView, OrderParamsValidatorMixin):
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


class ShopOrderWizardView(NamedUrlSessionWizardView):

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
        return super(ShopOrderWizardView, self).render(form, **kwargs)

    def done(self, form_list, **kwargs):
        pass
