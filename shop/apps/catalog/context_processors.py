# coding: utf-8


import json
from django.db.models import Max, Min
from leon.apps.base import BaseContextProcessor
from .base import ShopCatalogParamsValidatorMixin


PAGE_SIZE = 20
CATEGORY_GRID_COUNT = 6
MIN_PRICE = 0
MAX_PRICE = 9999999
MIN_STOCK = 0
MAX_STOCK = 9999999


class ShopCatalogMenuContextProcessor(BaseContextProcessor, ShopCatalogParamsValidatorMixin):
    """
    Class for block context processor menu
    """

    kwargs_params_slots = {
        'catalog_slug_title': [None, '']
    }

    CATEGORY_SITE_MODEL = None

    def _create_data(self):
        self.menu_catalog_category_s = self.CATEGORY_SITE_MODEL.get_root_nodes()
        self.menu_catalog_current_category = self.CATEGORY_SITE_MODEL.objects.filter(
            slug_title=self.params_storage['catalog_slug_title']).first()
        self.menu_catalog_parent_category = self.menu_catalog_current_category.get_parent()

        if not self.menu_catalog_parent_category:
            self.menu_catalog_parent_category = self.menu_catalog_current_category
            self.menu_catalog_parent_category.selected = True
        else:
            self.menu_catalog_parent_category.selected = False

    def __call__(self, request):
        self.main_menu = {}
        self.output_context = {
            'menu_catalog_category_s': None,
            'menu_catalog_current_category': None,
            'menu_catalog_parent_category': None
        }
        self._init(request)
        self._create_data()
        self._aggregate()
        return self.output_context


class ShopCatalogFilterContextProcessor(BaseContextProcessor, ShopCatalogParamsValidatorMixin):
    """
    Class for block context processor filter
    """

    request_params_slots = {
        'order': [None, 'default'],
        'page': [None, 1],
        'filter': [None, "{}"],
    }

    kwargs_params_slots = {
        'catalog_slug_title': [None, '']
    }

    CATEGORY_SITE_MODEL = None
    PRODUCT_MODEL = None
    PRODUCT_PARAMS_KV_MODEL = None
    FILTER_MODEL = None

    def _category_query(self):
        self.category_s = self.CATEGORY_SITE_MODEL.get_root_nodes()
        self.current_category = self.CATEGORY_SITE_MODEL.objects.filter(
            slug_title=self.params_storage['catalog_slug_title']).first()
        self.parent_category = self.current_category.get_parent()

        self.category_xml_s = list(self.current_category.category_xml_s.all().
                                   values_list('id', flat=True))
        for cat in self.current_category.get_children():
            self.category_xml_s.extend(cat.category_xml_s.all().
                                       values_list('id', flat=True))

    def _product_query(self):
        self.product_set = self.PRODUCT_MODEL.objects.filter(category_xml__in=self.category_xml_s)

    def _filter_query_s(self):
        """
        
        :return: 
        """
        qdata = json.loads(self.params_storage['filter'])
        self.filter_set = self.current_category.filter_s.all() or \
                          self.parent_category.filter_s.all()
        self.filter_set = self.filter_set

        for filter_obj in self.filter_set:
            filter_input = {'filter': filter_obj}
            params = qdata.get(filter_obj.type).get(filter_obj.code) if qdata.get(filter_obj.type) else {}
            if filter_obj.type == 'FIELD':
                q = filter_obj.query_method
                f = filter_obj.field_name
                if q:
                    filter_input = getattr(self, q)()
                else:
                    filter_input['max'] = int((self.product_set.aggregate(Max(f))
                                              ['{}__max'.format(f)] or 5) + 2)
                    filter_input['min'] = int((self.product_set.aggregate(Min(f))
                                              ['{}__min'.format(f)] or 5) - 2)
                    filter_input['from'] = params.get('from') or (filter_input['min'] + 1)
                    filter_input['to'] = params.get('to') or (filter_input['max'] - 1)
            if filter_obj.type in ['M2M', 'FK']:
                selected = str(params['selected']).split(',') if params.get('selected') else []
                q = filter_obj.query_method
                if q:
                    filter_input = getattr(self, q)(selected=selected)
                else:
                    obj_s = set(self.product_set.values_list(
                        '{0}__{0}__pk'.format(filter_obj.code),
                        '{0}__{0}__title'.format(filter_obj.code)))
                    obj_s.remove((None, None)) if (None, None) in obj_s else None
                    filter_input['item_s'] = [{'pk': k, 'title': v} for k, v in obj_s]
                    filter_input['selected'] = selected if selected \
                        else [item['pk'] for item in filter_input['item_s']]
            if filter_obj.type == 'KV':
                kv_key = filter_obj.kv_key
                selected = str(params['selected']).split(',') if params.get('selected') else []

                q = filter_obj.query_method
                if q:
                    filter_input = getattr(self, q)(selected=selected, kv_key=kv_key)
                else:
                    obj_s = set(self.product_set.filter(params_kv__key=kv_key).
                                values_list('params_kv__value_hash', 'params_kv__value'))
                    obj_s.remove((None, None)) if (None, None) in obj_s else None
                    filter_input['item_s'] = [{'pk': k, 'title': v} for k, v in obj_s]
                    filter_input['selected'] = selected if selected \
                        else [item['pk'] for item in filter_input['item_s']]
            self.filter_s.append(filter_input)

    def __call__(self, request):
        self.filter_s = []
        self.output_context = {
            'filter_s': None
        }
        self._init(request)
        self._category_query()
        self._product_query()
        self._filter_query_s()
        self._aggregate()
        return self.output_context
