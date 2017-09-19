# coding: utf-8


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
