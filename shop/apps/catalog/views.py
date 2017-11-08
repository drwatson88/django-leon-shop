# -*- coding: utf-8 -*-

import json
from digg_paginator import DiggPaginator
from django.shortcuts import get_object_or_404, HttpResponse

from .base import ShopCatalogBaseView, ShopCatalogParamsValidatorMixin


PAGE_SIZE = 20
CATEGORY_GRID_COUNT = 6
MIN_PRICE = 0
MAX_PRICE = 9999999
MIN_STOCK = 0
MAX_STOCK = 9999999


class ShopCategoryListView(ShopCatalogBaseView, ShopCatalogParamsValidatorMixin):

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
        super(ShopCategoryListView, self).__init__(*args, **kwargs)

    def _category_s_query(self, ):
        self.catalog_root_category_s = self.CATEGORY_SITE_MODEL.get_root_nodes().filter(show=True).all()

    def get(self, *args, **kwargs):
        self._category_s_query()
        return self._render()


class ShopProductListView(ShopCatalogBaseView, ShopCatalogParamsValidatorMixin):

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

        ALL PARAMS put in params_storage after validate
    """

    CATEGORY_SITE_MODEL = None
    PRODUCT_MODEL = None
    BRAND_MODEL = None
    BRAND_MAKER_MODEL = None
    PRODUCT_PARAMS_KV_MODEL = None
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
        'filter': [None, "{}"],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'current_category': None,
            'page': None,
        }
        super(ShopProductListView, self).__init__(*args, **kwargs)

    def _category_s_query(self):
        self.current_category = self.CATEGORY_SITE_MODEL.objects.filter(
            slug_title=self.params_storage['catalog_slug_title']).first()
        self.parent_category = self.current_category.get_parent()

        self.category_xml_s = list(self.current_category.category_xml_s.all().
                                   values_list('id', flat=True))
        for cat in self.current_category.get_children():
            self.category_xml_s.extend(cat.category_xml_s.all().
                                       values_list('id', flat=True))

    def _product_s_query(self):
        self.product_set = self.PRODUCT_MODEL.objects.filter(category_xml__in=self.category_xml_s)

    def _product_filter_s(self):
        """

        :return: 
        """
        qdata = json.loads(self.params_storage['filter'])
        if not qdata:
            return

        self.filter_set = self.current_category.filter_s.all() or \
                          (self.parent_category and self.parent_category.filter_s.all())
        self.filter_set = self.filter_set.order_by('position')

        for filter_obj in self.filter_set:
            params = qdata.get(filter_obj.type).get(filter_obj.code) if qdata.get(filter_obj.type) else {}
            if filter_obj.type == 'FIELD':
                q = filter_obj.query_method
                f = filter_obj.field_name
                if q:
                    self.product_set = getattr(self, q)()
                else:
                    if params.get('{}_from'.format(f)):
                        self.product_set = self.product_set.filter(
                            **{'{}_gte'.format(f): params.get('{}_from'.format(f))}
                        )
                    if params.get('{}_to'.format(f)):
                        self.product_set = self.product_set.filter(
                            **{'{}_lte'.format(f): params.get('{}_to'.format(f))}
                        )
            if filter_obj.type in ['M2M', 'FK']:
                selected = str(params['selected']).split(',') if params.get('selected') else []
                q = filter_obj.query_method
                if q:
                    self.product_set = getattr(self, q)(selected=selected)
                elif selected:
                    self.product_set = self.product_set.filter(**{'{}__in'.format(filter_obj.code): selected})

            if filter_obj.type == 'KV':
                selected = str(params['selected']).split(',') if params.get('selected') else []
                q = filter_obj.query_method
                kv_key = filter_obj.kv_key
                if q:
                    self.product_set = getattr(self, q)(selected=selected, kv_key=kv_key)
                elif selected:
                    self.product_set = self.product_set.filter(**{'params_kv__value_hash__in': selected})

    def _set_order_s(self):
        order = self.params_storage['order']
        self.order_s = self.ORDER_REFERENCE_MODEL.objects.order_by('-position').all()
        for order_obj in self.order_s:
            order_obj.selected = False
            if order_obj.code == order:
                order_obj.selected = True
        order_selected = self.ORDER_REFERENCE_MODEL.objects.get(code=order)
        self.order_name = order_selected.field_name \
            if order_selected.field_order else '-{}'.format(order_selected.field_name)
        self.product_set = self.product_set.order_by(self.order_name)

    def _product_s_pagination(self):
        paginator = DiggPaginator(self.product_set, self.page_size)
        self.page = paginator.page(self.params_storage['page'] or 1)

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._product_s_query()
        self._set_order_s()
        self._product_filter_s()
        self._product_s_pagination()
        self._aggregate()
        return self._render()


class ShopProductInsideView(ShopCatalogBaseView, ShopCatalogParamsValidatorMixin):

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

    kwargs_params_slots = {
        'product_slug_title': [None, ''],
    }

    request_params_slots = {
        'ajax': [None, 0],
        'product_stock': [None, 0],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'product': None
        }
        super(ShopProductInsideView, self).__init__(*args, **kwargs)

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
        # self._set_product_params_pack()
        # self._set_product_params_stock()
        # self._set_product_params_other()
        # self._set_product_image()
        # self._set_product_attach_image_s()
        # self._set_product_attach_file_s()
        # self._get_amount()
        self._aggregate()
        return self._render()


class ShopProductAddToBasketView(ShopCatalogBaseView, ShopCatalogParamsValidatorMixin):

    """ Product Inside View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. ITEM_S - cart item's with product_type, stock, price,
        print_type

        ALL PARAMS put in params_storage after validate
    """

    PRODUCT_MODEL = None
    BASKET_CONTAINER = None

    request_params_slots = {
        'item_s': [None, 0]
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'total_price': None
        }
        super(ShopProductAddToBasketView, self).__init__(*args, **kwargs)
        self.item_s = None
        self.total_price = None

    def _calc_update(self):
        basket = self.BASKET_CONTAINER(self.request.session, self.request.user)
        self.item_s = json.loads(self.params_storage['item_s'])
        total_price = 0
        for item in self.item_s:
            product = self.PRODUCT_MODEL.objects.get(pk=item['pk'])
            quantity = int(item['stock'])
            total_price += product.price * quantity
            basket.add_item(product, quantity)
        self.total_price = str(abs(total_price))

    def get(self, *args, **kwargs):
        self._calc_update()
        self._aggregate()
        return HttpResponse(json.dumps(self.output_context))


class ShopProductInsideCalcView(ShopCatalogBaseView, ShopCatalogParamsValidatorMixin):

    """ Product Inside View. Receives get params
        and response neither arguments in get
        request params.

        GET Params:

        1. ITEM_S - cart item's with product_type, stock, price,
        print_type

        ALL PARAMS put in params_storage after validate
    """

    PRODUCT_MODEL = None

    request_params_slots = {
        'item_s': [None, 0]
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'total_price': None
        }
        super(ShopProductInsideCalcView, self).__init__(*args, **kwargs)
        self.item_s = None
        self.total_price = None

    def _calc_update(self):
        self.item_s = json.loads(self.params_storage['item_s'])
        total_price = 0
        for item in self.item_s:
            product = self.PRODUCT_MODEL.objects.get(pk=item['pk'])
            quantity = int(item['stock'])
            total_price += product.price * quantity
        self.total_price = str(abs(total_price))

    def get(self, *args, **kwargs):
        self._calc_update()
        self._aggregate()
        return HttpResponse(json.dumps(self.output_context))

