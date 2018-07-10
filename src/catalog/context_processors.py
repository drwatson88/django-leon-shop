# coding: utf-8


"""
.. module:: catalog
    :platform: Unix
    :synopsis: module illustrating how to document python source code

.. moduleauthor:: Patrick Kennedy <patkennedy79@gmail.com>
"""


import json
import re
from django.db.models import Max, Min
from leon_base.base.context_processors import BaseContextProcessor
from .base import ShopCatalogParamsValidatorMixin


PAGE_SIZE = 20
PAGE_COUNTER_S = [9, 18, 30, 60, 90]
CATEGORY_GRID_COUNT = 6
MIN_PRICE = 0
MAX_PRICE = 9999999
MIN_STOCK = 0
MAX_STOCK = 9999999


class ShopCatalogMenuContextProcessor(BaseContextProcessor, ShopCatalogParamsValidatorMixin):
    """Class illustrating how to document python source code

        This class provides some basic methods for incrementing, decrementing,
        and clearing a number.

        .. note::

        This class does not provide any significant functionality that the
        python does not already include. It is just for illustrative purposes.
    """
    kwargs_params_slots = {
        'catalog_slug_title': [None, '']
    }

    CATEGORY_SITE_MODEL = None
    NAV_MENU_LIMIT = 10

    def _create_data(self):
        """A simple initialization method.

            Args:
            None
        """
        self.category_s = self.CATEGORY_SITE_MODEL.get_root_nodes()
        self.current = self.CATEGORY_SITE_MODEL.objects.filter(
            slug_title=self.params_storage['catalog_slug_title']).first()
        self.parent = self.current.get_parent() if self.current else {}

        if not self.parent and self.current:
            self.parent = self.current
            self.parent.selected = True
        self.catalog_menu = {
            'nav_next_set': self._nav_next_set,
            'category_s': self.category_s,
            'current': self.current,
            'parent': self.parent
        }

    def _nav_next_set(self):
        for i in range(len(self.category_s) // self.NAV_MENU_LIMIT + 1):
            cat_set = self.category_s[i*self.NAV_MENU_LIMIT:(i+1)*self.NAV_MENU_LIMIT]
            yield zip(cat_set, range(len(cat_set))), i

    def __call__(self, request):
        self.catalog_menu = {}
        self.output_context = {
            'catalog_menu': None
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
        'filter': [None, {}],
        'count': [None, PAGE_COUNTER_S[0]]
    }

    kwargs_params_slots = {
        'catalog_slug_title': [None, '']
    }

    CATEGORY_SITE_MODEL = None
    PRODUCT_MODEL = None
    FILTER_PARAMSKV_GROUP_MODEL = None
    PRODUCT_PARAMS_KV_MODEL = None
    ORDER_REFERENCE_MODEL = None

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

    def _category_s_cache(self):
        self.current_category = self.CATEGORY_SITE_MODEL.objects.filter(
            slug_title=self.params_storage['catalog_slug_title']).first()
        self.parent_category = self.current_category.get_parent()
        self.category_xml_s = json.loads(self.current_category.category_xml_cache)

    def _product_query(self):
        self.product_set = self.PRODUCT_MODEL.objects.filter(category_xml__in=self.category_xml_s)

    def _filter_query_s(self):
        """
        
        :return: 
        """
        qdata = self.params_storage['filter']

        self.filter_s = []
        level = self.current_category.depth
        current_category = self.current_category
        for i in reversed(range(level)):
            self.filter_set = current_category.filter_s.exclude(type=['KV']).all()
            if self.filter_set:
                break
            current_category = current_category.get_parent()

        for filter_obj in self.filter_set:
            filter_input = {'filter': filter_obj}
            params = qdata.get(filter_obj.type).get(filter_obj.code) if qdata.get(filter_obj.type) else {}
            if filter_obj.type == 'FIELD':
                q = filter_obj.query_method
                f = filter_obj.field_name
                u = filter_obj.unit
                if q:
                    filter_input = getattr(self, q)()
                else:
                    filter_input['max'] = int((self.product_set.aggregate(Max(f))
                                              ['{}__max'.format(f)] or 5) + 2)
                    filter_input['min'] = int((self.product_set.aggregate(Min(f))
                                              ['{}__min'.format(f)] or 5) - 2)
                    filter_input['from'] = params.get('from') or (filter_input['min'] + 1)
                    filter_input['to'] = params.get('to') or (filter_input['max'] - 1)
                    filter_input['unit'] = u
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
                    filter_input['selected'] = [int(i) for i in selected] if selected \
                        else [item['pk'] for item in filter_input['item_s']]
            self.filter_s.append(filter_input)

        self.filter_set = self.current_category.filter_s.filter(type=['KV']).all()
        for filter_obj in self.filter_set:
            filter_input = {'filter': filter_obj}
            params = qdata.get(filter_obj.type, {}).get(filter_obj.code, {})
            selected = str(params['selected']).split(',') if params.get('selected') else []

            obj_s = zip(json.loads(self.FILTER_PARAMSKV_GROUP_MODEL.objects.
                                   filter(filter=filter_obj, category_site=self.current_category).value_hash),
                        json.loads(self.FILTER_PARAMSKV_GROUP_MODEL.objects.
                                   filter(filter=filter_obj, category_site=self.current_category).value))
            filter_input['item_s'] = [{'pk': k, 'title': v} for k, v in obj_s]
            filter_input['selected'] = selected
            self.filter_s.append(filter_input)

    def _order_query_s(self):
        self.order = {}
        order_param = self.params_storage['order']
        self.order['order_s'] = self.ORDER_REFERENCE_MODEL.objects.order_by('-position').all()
        self.order['selected'] = order_param \
            if order_param else 'default'

    def _counter_query_s(self):
        self.counter = {}
        count_param = self.params_storage['count']
        self.counter['count_s'] = [{'code': i, 'title': i} for i in PAGE_COUNTER_S]
        self.counter['selected'] = count_param if count_param else 'ALL'

    def __call__(self, request):
        self.filter_s = []
        self.output_context = {
            'filter_s': None,
            'order': None,
            'counter': None
        }
        self._init(request)
        self._category_s_cache()
        self._product_query()
        self._filter_query_s()
        self._order_query_s()
        self._counter_query_s()
        self._aggregate()
        return self.output_context


class ShopCatalogBreadcrumbContextProcessor(BaseContextProcessor):

    """
    Class for breadcrumb context processor menu
    """

    PRODUCT_MODEL = None
    CATEGORY_MODEL = None

    def _init(self, request):
        super(ShopCatalogBreadcrumbContextProcessor, self)._init(request)
        self.request = request

    def _create_data(self):
        self.breadcrumb_s = []
        self._parse_url()
        self.breadcrumb_s.append({
            'title': 'Каталог',
            'url': '/'
        })
        self.breadcrumb_s = reversed(self.breadcrumb_s)

    def _parse_url(self):
        ptn = re.compile(r'/(?P<section>\w+)/(?P<object_slug>.+)//?')
        match = ptn.match(self.request.path)
        gd = match.groupdict() if match else {}
        section = gd.get('section')
        object_slug = gd.get('object_slug', '')

        if section == 'product':
            self._set_product(object_slug)
        if section == 'category':
            self._set_category(object_slug)

    def _set_product(self, slug):
        try:
            product = self.PRODUCT_MODEL.objects.get(slug_title=slug)
        except:
            raise

        self.breadcrumb_s.append({
            'title': product.title,
            'url': None
        })

        xml_cat = product.category_xml.first()
        last_cat = xml_cat.category_site if xml_cat else None
        if last_cat:
            self.breadcrumb_s.append({
                'title': last_cat.title,
                'url': last_cat.get_absolute_url()
            })
            for i in range(1, last_cat.depth):
                last_cat = last_cat.get_parent()
                self.breadcrumb_s.append({
                    'title': last_cat.title,
                    'url': last_cat.get_absolute_url()
                })

    def _set_category(self, slug):
        try:
            category = self.CATEGORY_MODEL.objects.get(slug_title=slug)
        except:
            raise

        last_cat = category
        if last_cat:
            self.breadcrumb_s.append({
                'title': last_cat.title,
                'url': ''
            })
            for i in range(1, last_cat.depth):
                last_cat = last_cat.get_parent()
                self.breadcrumb_s.append({
                    'title': last_cat.title,
                    'url': last_cat.get_absolute_url()
                })

    def _popup(self):
        return 'popup' in self.request.path

    def __call__(self, request):
        self.header = {}
        self.output_context = {
            'breadcrumb_s': None
        }
        self._init(request)
        if self._popup():
            return {}
        self._create_data()
        self._aggregate()
        return self.output_context


class ShopCatalogSidebarMenuContextProcessor(BaseContextProcessor):

    """
    Class for sidebar context processor menu
    """

    CATEGORY_SITE_MODEL = None

    def _init(self, request):
        super(ShopCatalogSidebarMenuContextProcessor, self)._init(request)
        self.request = request

    def _parse_url(self):
        ptn = re.compile(r'/category/(?P<object_slug>.+)//?')
        match = ptn.match(self.request.path)
        gd = match.groupdict() if match else {}
        self.object_slug = gd.get('object_slug', '')

    def _set_category(self):
        category = self.CATEGORY_SITE_MODEL.objects.get(slug_title=self.object_slug)
        self.sidebar_category_s = category.get_children()

    def _popup(self):
        return 'popup' in self.request.path

    def __call__(self, request):
        self.header = {}
        self.output_context = {
            'sidebar_category_s': None
        }
        self._init(request)
        if self._popup():
            return {}
        self._parse_url()
        self._set_category()
        self._aggregate()
        return self.output_context
