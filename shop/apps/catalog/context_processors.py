# coding: utf-8


import json
from django.db.models import Max, Min
from leon.base import BaseContextProcessor
from catalog.base import CatalogParamsValidatorMixin


class CategoryMenuContextProcessor(BaseContextProcessor, CatalogParamsValidatorMixin):
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


class CategoryFilterContextProcessor(BaseContextProcessor, CatalogParamsValidatorMixin):
    """
    Class for block context processor filter
    """

    request_params_slots = {
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
        for cat in self.current_category.get_childrens():
            self.category_xml_s.extend(cat.category_xml_s.all().
                                       values_list('id', flat=True))

    def _product_query(self):
        self.product_set = self.PRODUCT_MODEL.objects.filter(category_xml__in=self.category_xml_s)

    def _filter_s(self):
        """
        
        :return: 
        """

        self.filter_set = self.current_category.filters.all() or \
                        self.parent_category.filters.all()
        self.filter_set = self.filter_set.order_by('position')

        for filter_obj in self.filter_set:
            filter_input = {'type': filter_obj.type}
            if filter_obj.type == 'PRICE':
                filter_input['price_max'] = self.product_set.aggregate(Max('price'))
                filter_input['price_min'] = self.product_set.aggregate(Min('price'))
                filter_input['price_from'] = self.params_storage['price_from'] or filter_input['price_min']
                filter_input['price_to'] = self.params_storage['price_to'] or filter_input['price_max']
            if filter_obj.type == 'STOCK':
                # TODO: продумать скидку
                filter_input['stock_max'] = self.product_set.aggregate(Max('stock'))
                filter_input['stock_min'] = self.product_set.aggregate(Min('stock'))
                filter_input['stock_from'] = self.params_storage['stock_from'] or filter_input['stock_min']
                filter_input['stock_to'] = self.params_storage['stock_to'] or filter_input['stock_max']
            if filter_obj.type in ['M2M', 'FK']:
                json_value = json.loads(filter_obj.value)
                filter_input['selected'] = self.params_storage.get(json_value['param']).split(',')
                filter_input['item_s'] = getattr(self.current_category, json_value['related_query']).\
                    values('id', 'title')
            if filter_obj.type == 'KV':
                json_value = json.loads(filter_obj.value)
                product_id_s = self.product_set.values_list('id', flat=True)
                value_s = self.PRODUCT_PARAMS_KV_MODEL.objects.\
                    filter({'{rel}__in'.format(rel=json_value['related_query']): product_id_s}).\
                    filter(abbr=filter_obj.name)
                filter_input['selected'] = value_s.filter(value=self.params_storage[json_value['abbr']])
                filter_input['item_s'] = value_s.all()
            self.filter_s.append(filter_input)

    def __call__(self, request):
        self.filter_s = []
        self.output_context = {
            'filter_s': None
        }
        self._init(request)
        self._category_query()
        self._product_query()
        self._filter_s()
        self._aggregate()
        return self.output_context
