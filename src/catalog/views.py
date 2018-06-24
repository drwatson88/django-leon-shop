# -*- coding: utf-8 -*-


import json
from digg_paginator import DiggPaginator
from django.shortcuts import get_object_or_404, HttpResponse, redirect
from django.http import JsonResponse, Http404

from .base import ShopCatalogBaseView, ShopCatalogParamsValidatorMixin


PAGE_SIZE = 20
PAGE_COUNTER_S = [9, 18, 30, 60, 90]
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
    template_popup_change = {}

    kwargs_params_slots = {
        'catalog_slug_title': [None, ''],
    }

    request_params_slots = {
        'order': [None, 'default'],
        'page': [None, 1],
        'filter': [None, {}],
        'count': [None, PAGE_COUNTER_S[0]],
        'grid': [None, 0]
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'current_category': None,
            'page': None,
            'canonical': None
        }
        super(ShopProductListView, self).__init__(*args, **kwargs)

    def _category_s_query(self):
        self.current_category = self.CATEGORY_SITE_MODEL.objects.filter(
            slug_title=self.params_storage['catalog_slug_title']).first()
        if not self.current_category:
            raise Http404
        self.parent_category = self.current_category.get_parent()

        self.category_xml_s = list(self.current_category.category_xml_s.all().
                                   values_list('id', flat=True))
        for cat in self.current_category.get_children():
            self.category_xml_s.extend(cat.category_xml_s.all().
                                       values_list('id', flat=True))

    def _category_s_cache(self):
        self.current_category = self.CATEGORY_SITE_MODEL.objects.filter(
            slug_title=self.params_storage['catalog_slug_title']).first()
        if not self.current_category:
            raise Http404
        self.parent_category = self.current_category.get_parent()
        self.category_xml_s = json.loads(self.current_category.category_xml_cache)

    def _product_s_query(self):
        self.product_set = self.PRODUCT_MODEL.objects.filter(category_xml__in=self.category_xml_s)

    def _product_filter_s(self):
        """

        :return: 
        """
        qdata = self.params_storage['filter']
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
                    if params.get('from'):
                        self.product_set = self.product_set.filter(
                            **{'{}__gte'.format(f): params.get('from')}
                        )
                    if params.get('to'):
                        self.product_set = self.product_set.filter(
                            **{'{}__lte'.format(f): params.get('to')}
                        )
            if filter_obj.type in ['M2M', 'FK']:
                selected = str(params['selected']).split(',') if params.get('selected') else []
                q = filter_obj.query_method
                if q:
                    self.product_set = getattr(self, q)(selected=selected)
                elif selected:
                    self.product_set = self.product_set.\
                        filter(**{'{0}__{0}__pk__in'.format(filter_obj.code): [int(i) for i in selected]})

            if filter_obj.type == 'KV':
                selected = str(params['selected']).split(',') if params.get('selected') else []
                q = filter_obj.query_method
                kv_key = filter_obj.kv_key
                if q:
                    self.product_set = getattr(self, q)(selected=selected, kv_key=kv_key)
                elif selected:
                    self.product_set = self.product_set.filter(**{'params_kv__value_hash__in': selected})

    def _set_order_s(self):
        order_param = self.params_storage['order'] or 'default'
        order_selected = self.ORDER_REFERENCE_MODEL.objects.get(code=order_param)
        order_name = order_selected.field_name \
            if order_selected.field_order else '-{}'.format(order_selected.field_name)
        self.product_set = self.product_set.order_by(order_name)

    def _product_s_pagination(self):
        count = self.params_storage['count']
        count = count if count != 'ALL' else None

        if count:
            paginator = DiggPaginator(self.product_set, self.params_storage['count'])
            page = int(self.params_storage['page'] or 1)
            if paginator.num_pages < page:
                raise Http404
            self.page = paginator.page(page)
        else:
            self.page = {'object_list': self.product_set}

    def _set_view_template(self):
        if self.popup:
            self.template_popup['grid'] = self.template_popup_change.get(
                'list' if self.params_storage['grid'] else 'grid')

    def _set_canonical(self):
        self.canonical = self.current_category.get_absolute_url()

    def get(self, *args, **kwargs):
        # self._category_s_query()
        self._category_s_cache()
        self._product_s_query()
        self._product_filter_s()
        self._set_order_s()
        self._product_s_pagination()
        self._set_view_template()
        self._set_canonical()
        self._aggregate()
        return self._render()


class ShopProductSaleListView(ShopCatalogBaseView, ShopCatalogParamsValidatorMixin):

    """ Product Sale List View. Receives get params
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

    PRODUCT_MODEL = None
    BRAND_MODEL = None
    BRAND_MAKER_MODEL = None
    PRODUCT_PARAMS_KV_MODEL = None
    ORDER_REFERENCE_MODEL = None
    FILTER_MODEL = None

    page_size = PAGE_SIZE
    context_processors = []
    template_popup_change = {}

    kwargs_params_slots = {
    }

    request_params_slots = {
        'order': [None, 'default'],
        'page': [None, 1],
        'filter': [None, {}],
        'count': [None, PAGE_COUNTER_S[0]],
        'grid': [None, 0]
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'page': None,
        }
        super(ShopProductSaleListView, self).__init__(*args, **kwargs)

    def _product_s_query(self):
        self.product_set = self.PRODUCT_MODEL.objects.filter(sale=True)

    def _set_order_s(self):
        order_param = self.params_storage['order'] or 'default'
        order_selected = self.ORDER_REFERENCE_MODEL.objects.get(code=order_param)
        order_name = order_selected.field_name \
            if order_selected.field_order else '-{}'.format(order_selected.field_name)
        self.product_set = self.product_set.order_by(order_name)

    def _product_s_pagination(self):
        count = self.params_storage['count']
        count = count if count != 'ALL' else None

        if count:
            paginator = DiggPaginator(self.product_set, self.params_storage['count'])
            self.page = paginator.page(self.params_storage['page'] or 1)
        else:
            self.page = {'object_list': self.product_set}

    def _set_view_template(self):
        if self.popup:
            self.template_popup['grid'] = self.template_popup_change.get(
                'list' if self.params_storage['grid'] else 'grid')

    def get(self, *args, **kwargs):
        self._product_s_query()
        self._set_order_s()
        self._product_s_pagination()
        self._set_view_template()
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
        item_s = json.loads(self.params_storage['item_s'])
        total_price = 0
        for item in item_s:
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
        'product': [None, {}]
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'product_total': None
        }
        super(ShopProductInsideCalcView, self).__init__(*args, **kwargs)
        self.item_s = None
        self.product_total = None

    def _calc_update(self):
        item_s = self.params_storage['product'].get('item_s')
        total_price = 0
        for item in item_s:
            product = self.PRODUCT_MODEL.objects.get(pk=item['pk'])
            quantity = int(item['stock'])
            total_price += product.price * quantity
        self.product_total = str(abs(total_price))

    def get(self, *args, **kwargs):
        self._calc_update()
        self._aggregate()
        return JsonResponse(self.output_context)
