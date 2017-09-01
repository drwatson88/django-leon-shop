# -*- coding: utf-8 -*-

import json
from digg_paginator import DiggPaginator
from django.utils.decorators import classonlymethod
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, HttpResponse

from cart.cart import Cart
from .models import CategorySite, Product, Brand, BrandMaker, PrintType, \
    PrintTypeMaker, OrderReference
from .base import CatalogBaseView, CatalogParamsValidatorMixin


PAGE_SIZE = 20
CATEGORY_GRID_COUNT = 6
MIN_PRICE = 0
MAX_PRICE = 9999999
MIN_STOCK = 0
MAX_STOCK = 9999999


class CategoryListView(CatalogBaseView, CatalogParamsValidatorMixin):

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

    CATEGORY_SITE_MODEL = None

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'catalog_root_category_s': None
        }
        super(CategoryListView, self).__init__(*args, **kwargs)

    def _category_s_query(self, ):
        self.root_category_s = self.CATEGORY_SITE_MODEL.get_root_nodes().filter(show=True).all()

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._aggregate()
        return self._render()


class ProductListView(CatalogBaseView, CatalogParamsValidatorMixin):

    """ Product List View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. AJAX - if ajax is True, we have response
        html part, that insert in DOM structure in client
        side. If we have True, we response all html
        document with base template.
        2. GRID - grid or list
        3. GRID_CNT - count columns in grid
        4. ORDER - sort order
        5. PAGE_NO - page number
        6. PAGE_SIZE - size of page (count = rows*columns)
        7. BRAND_ID_S - list of id's in database of site brands

        ALL PARAMS put in params_storage after validate
    """

    CATEGORY_SITE_MODEL = None
    PRODUCT_MODEL = None
    BRAND_MODEL = None
    BRAND_MAKER_MODEL = None
    ORDER_REFERENCE_MODEL = None
    FILTER_MODEL = None

    page_size = PAGE_SIZE
    context_processors = []

    kwargs_params_slots = {
        'catalog_slug_title': [None, ''],
    }

    request_params_slots = {
        'order': [None, 'default'],

        'page': [None, 1],

        'price_from': [None, MIN_PRICE],
        'price_to': [None, MAX_PRICE],

        'stock_from': [None, MIN_STOCK],
        'stock_to': [None, MAX_STOCK],

        'brand_id_s': [None, []],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'page': None,
        }
        super(ProductListView, self).__init__(*args, **kwargs)

    def _category_s_query(self):
        current_category = self.CATEGORY_SITE_MODEL.objects.filter(
                slug_title=self.params_storage['catalog_slug_title']).first()

        self.category_xml_s = list(current_category.category_xml_s.all().
                                   values_list('id', flat=True))
        for cat in current_category.get_childrens():
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
            if filter_obj.type == 'PRICE':
                if self.params_storage['price_from']:
                    self.product_set = self.product_set.filter(price__gte=self.params_storage['price_from'])
                if self.params_storage['price_to']:
                    self.product_set = self.product_set.filter(price__gte=self.params_storage['price_to'])
            if filter_obj.type == 'STOCK':
                if self.params_storage['stock_from']:
                    self.product_set = self.product_set.filter(stock__gte=self.params_storage['stock_from'])
                if self.params_storage['stock_to']:
                    self.product_set = self.product_set.filter(stock__gte=self.params_storage['stock_to'])
            if filter_obj.type in ['M2M', 'FK']:
                json_value = json.loads(filter_obj.value)
                filter_value = self.params_storage.get(filter_obj.name) or \
                               (json_value['filter'] and self.params_storage[json_value['filter']])

                if filter_value:
                    self.product_set = self.product_set.\
                        filter(**{'{abbr}__value'.format(abbr=filter_obj.name): filter_value})

            if filter_obj.type == 'KV':
                json_value = json.loads(filter_obj.value)
                filter_value = self.params_storage.get(filter_obj.name) or \
                               (json_value['filter'] and self.params_storage[json_value['filter']])

                if filter_value:
                    product_id_s = self.product_set.values_list('id', flat=True)
                    product_kv_id_s = self.CATALOG_PRODUCT_PARAMS_KV_MODEL.objects. \
                        filter(**{'{rel}__in'.format(rel=json_value['related_query']): product_id_s}). \
                        filter(abbr=filter_obj.name).\
                        filter(value=filter_value).\
                        values('{rel}__pk'.format(rel=json_value['related_query']), flat=True)
                    self.product_set = self.product_set.filter(pk__in=product_kv_id_s)

    def _brand_s_query(self):
        brand_id_s = self.params_storage['brand_id_s']
        self.brand_obj_s = self.BRAND_MODEL.objects.all()
        for brand_obj in self.brand_obj_s:
            if str(brand_obj.id) in brand_id_s:
                brand_obj.checked = True
        self.brand_maker_id_s = self.BRAND_MAKER_MODEL.objects.filter(brand__in=brand_id_s). \
            values_list('id', flat=True)

    def _set_order_s(self):
        order = self.params_storage['order']
        self.order_s = self.ORDER_REFERENCE_MODEL.objects.order_by('-position').all()
        for order_obj in self.order_s:
            order_obj.selected = False
            if order_obj.name == order:
                order_obj.selected = True
        order_selected = self.ORDER_REFERENCE_MODEL.objects.get(name=order)
        self.order_name = order_selected.field_name \
            if order_selected.field_order else '-{}'.format(order_selected.field_name)

    def _product_obj_s_query(self):
        self.product_obj_s_query = self.PRODUCT_MODEL.objects.filter(category_xml__in=self.category_xml_s)

    def _product_s_query(self):
        paginator = DiggPaginator(self.product_obj_s_query, self.page_size)
        self.page = paginator.page(self.params_storage['page'] or 1)

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._brand_s_query()
        self._print_type_s_query()
        self._set_order_s()
        self._product_obj_s_query()
        self._product_filter()
        self._product_s_query()
        self._aggregate()
        return self._render()


class ProductInsideView(CatalogBaseView, CatalogParamsValidatorMixin):

    """ Product Inside View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. AJAX - if ajax is True, we have response
        html part, that insert in DOM structure in client
        side. If we have True, we response all html
        document with base template.
        2. PRODUCT_STOCK - stock count of products

        ALL PARAMS put in params_storage after validate
    """

    PRODUCT_MODEL = None

    request_params_slots = {
        'ajax': [None, 0],
        'product_stock': [None, 0],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'product': None
        }
        super(ProductInsideView, self).__init__(*args, **kwargs)

    def _set_product(self):
        self.product = get_object_or_404(self.PRODUCT_MODEL,
                                         slug_title=self.params_storage['product_slug_title'])

    def _set_product_params_pack(self):
        self.product.params_pack = []
        for pack_param in self.product.productparamspack_set.filter(pack_id=0).\
                order_by('position').all():
            self.product.params_pack.append({'name': pack_param.name,
                                             'value': pack_param.value})

    def _set_product_params_stock(self):
        self.product.params_stock = []
        for stock_param in self.product.productparamsstock_set.order_by('position').all():
            self.product.params_stock.append({'name': stock_param.name,
                                              'value': stock_param.value})

    def _set_product_params_other(self):
        self.product.params_other = []
        for other_param in self.product.productparamsother_set.order_by('position').all():
            self.product.params_other.append({'name': other_param.name,
                                              'value': other_param.value})

    def _set_product_image(self):
        self.product.image_current = \
            self.product.super_big_image or \
            self.product.big_image or \
            self.product.small_image

    def _set_product_attach_image_s(self):
        self.product.attach_images = self.product.productattachment_set.filter(meaning=1)

    def _set_product_attach_file_s(self):
        self.product.attach_files = self.product.productattachment_set.filter(meaning=0)

    def _get_amount(self):
        self.total_price = 0

    def get(self, *args, **kwargs):
        self._set_product()
        self._category_s_query()
        self._set_product_params_pack()
        self._set_product_params_stock()
        self._set_product_params_other()
        self._set_product_image()
        self._set_product_attach_image_s()
        self._set_product_attach_file_s()
        self._get_amount()
        self._aggregate()
        return self._render()


class ProductCalcView(CatalogBaseView, CatalogParamsValidatorMixin):

    """ Product Inside View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. AJAX - if ajax is True, we have response
        html part, that insert in DOM structure in client
        side. If we have True, we response all html
        document with base template.
        2. ITEM_S - cart item's with product_type, stock, price,
        print_type

        ALL PARAMS put in params_storage after validate
    """

    request_params_slots = {
        'ajax': [None, 0],
        'item_s': [None, 0],
        'cart': [None, None],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'total_price': None
        }
        super(ProductCalcView, self).__init__(*args, **kwargs)
        self.item_s = None
        self.total_price = None

    def calc_update(self):
        self.item_s = json.loads(self.params_storage['item_s'])
        total_price = 0
        for item in self.item_s:
            product = Product.objects.get(pk=item['pk'])
            quantity = int(item['stock'])
            total_price += product.price * quantity
        self.total_price = str(abs(total_price))

    def get(self, *args, **kwargs):
        self.calc_update()
        self._aggregate()
        return HttpResponse(json.dumps(self.output_context))

