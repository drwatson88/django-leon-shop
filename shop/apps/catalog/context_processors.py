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

        'price_from': [None, None],
        'price_to': [None, None],

        'stock_from': [None, None],
        'stock_to': [None, None],

        'brand_id_s': [None, []],
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
            if filter_obj.type == 'FIELD':
                params = qdata[filter_obj.type][filter_obj.code]
                q = filter_obj.query_method
                if q:
                    getattr(self, q)()
                else:
                    filter_input['max'] = int(self.product_set.aggregate(Max(filter_obj.field_name))
                                              ['{}__max'.format(filter_obj.field_name)] + 2)
                    filter_input['min'] = int(self.product_set.aggregate(Min(filter_obj.field_name))
                                              ['{}__min'.format(filter_obj.field_name)] - 2)
                    filter_input['from'] = params['from'] or (filter_input['min'] + 1)
                    filter_input['to'] = params['to'] or (filter_input['max'] - 1)
            if filter_obj.type in ['M2M', 'FK']:
                m = filter_obj.query_method
                f = filter_obj.query_filter
                filter_input['item_s'] = getattr(self, m)(query_filter=f)
                filter_input['selected'] = self._get_format_param(f)
            if filter_obj.type == 'KV':
                key = filter_obj.key
                f = filter_obj.query_filter
                filter_input['item_s'] = self._param_kv_s_query(key=key)
                filter_input['selected'] = self._get_format_param(f)
            self.filter_s.append(filter_input)

    def _get_format_param(self, param):
        param = str(self.params_storage[param]) or ''
        return json.loads(param) if param and len(param.split(',')) > 1 else [param] if param else []

    def _brand_s_query(self, *args, **kwargs):
        brand_s = set(self.product_set.values_list('brand__brand__pk', 'brand__brand__title'))
        brand_s.remove((None, None)) if (None, None) in brand_s else None
        return [{'pk': k, 'title': v} for k, v in brand_s]

    def _param_kv_s_query(self, *args, **kwargs):
        key = kwargs['key']
        brand_s = set(self.product_set.filter(params_kv__key=key).
                      values_list('params_kv__value_hash', 'params_kv__value'))
        brand_s.remove((None, None))
        return brand_s

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
