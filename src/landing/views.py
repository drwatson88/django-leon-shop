# coding: utf-8


from django.http import Http404
from .base import LandingBaseView, LandingParamsValidatorMixin


class ShopLandingView(LandingBaseView, LandingParamsValidatorMixin):

    """ Landing View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. AJAX - if ajax is True, we have response
        html part, that insert in DOM structure in client
        side. If we have True, we response all html
        document with base template.

        ALL PARAMS put in params_storage after validate
    """

    LANDING_MODEL = None

    kwargs_params_slots = {
        'landing_slug_title': [None, ''],
    }

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'landing': None
        }
        super(ShopLandingView, self).__init__(*args, **kwargs)

    def _get_landing(self):
        self.landing = self.LANDING_MODEL.objects.filter(slug_title=self.params_storage['landing_slug_title']).first()
        if not self.landing:
            raise Http404

    def _set_template(self):
        self.template_name = self.landing.template

    def get(self, *args, **kwargs):
        self._get_landing()
        self._set_template()
        self._aggregate()
        return self._render()
