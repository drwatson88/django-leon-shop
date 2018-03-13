# coding: utf-8

import json
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse
from django.db.models.query_utils import Q
from .base import SearchBaseView, SearchParamsValidatorMixin


class ShopSearchLookupView(SearchBaseView, SearchParamsValidatorMixin):

    """ Search View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. AJAX - if ajax is True, we have response
        html part, that insert in DOM structure in client
        side. If we have True, we response all html
        document with base template.
        2. ITEM_S - list of dicts of items with params
        (
            id: id of product/subproduct
        )

        ALL PARAMS put in params_storage after validate
    """

    STRING_LIMIT = 100
    LOOKUP_LIMIT = 10
    PRODUCT_MODEL = None

    request_params_slots = {
        'query': [None, ''],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'lookup_obj_s': None
        }
        super(ShopSearchView, self).__init__(*args, **kwargs)

    def _set_query(self):
        self._query = self.params_storage['query']

    def _set_item_set(self):
        self.item_set = self.PRODUCT_MODEL.objects.filter(
            Q(title__icontains=self._query) | Q(code__icontains=self._query)
        ).all().order_by('title')[:self.LOOKUP_LIMIT]

    def _set_lookup(self):
        self.lookup_obj_s = \
            [{'pk': p.pk, 'name': '{} - {}'.format(p.code, p.title)[:self.STRING_LIMIT]} for p in self.item_set]

    def get(self, *args, **kwargs):
        self._set_query()
        self._set_item_set()
        self._set_lookup()
        self._aggregate()
        return HttpResponse(json.dumps(self.output_context))


class ShopSearchListView(SearchBaseView, SearchParamsValidatorMixin):

    PRODUCT_MODEL = None
    
    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'search_set': None
        }
        super(ShopSearchView, self).__init__(*args, **kwargs)

    def _set_query(self):
        self._query = self.params_storage['query']

    def _set_item_set(self):
        self.search_set = self.PRODUCT_MODEL.objects.filter(
            Q(title__icontains=self._query) | Q(code__icontains=self._query)
        ).all().order_by('title')[:self.LOOKUP_LIMIT]

    def get(self, *args, **kwargs):
        self._set_query()
        self._set_item_set()
        self._aggregate()
        return self._render()

