

from importlib import import_module
from django.conf import settings


from django.utils.deprecation import MiddlewareMixin


class ShopBasketSessionMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        self.get_response = get_response
        engine = import_module(settings.SESSION_ENGINE)
        self.session_store = engine.SessionStore()

    def process_request(self, request):
        key = request.session.session_key
        if not key or not self.session_store.exists(key):
            obj = request.session.create_model_instance({})
            obj.save()
        request.session.save()
