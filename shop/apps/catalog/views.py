# -*- coding: utf-8 -*-

import json
from digg_paginator import DiggPaginator
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse

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

    request_params_slots = {
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'root_category_s': None
        }
        super(CategoryListView, self).__init__(*args, **kwargs)

    def _category_s_query(self, ):
        self.root_category_s = CategorySite.get_root_nodes().filter(show=True).all()

    def _aggregate(self):
        for item in self.output_context:
            self.output_context[item] = getattr(self, item)

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._aggregate()
        return render_to_response(
            self._get_template(),
            self.output_context,
            context_instance=RequestContext(self.request), )


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

    page_size = PAGE_SIZE

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
        'print_type_id_s': [None, []],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'page': None,
        }
        super(ProductListView, self).__init__(*args, **kwargs)

    def _category_s_query(self):
        current_category = CategorySite.objects.filter(
                slug_title=self.params_storage['catalog_slug_title']).first()

        self.category_xml_s = list(self.current_category.category_xml_s.all().
                                   values_list('id', flat=True))
        for cat in current_category.get_childrens():
            self.category_xml_s.extend(cat.category_xml_s.all().
                                       values_list('id', flat=True))

    def _brand_s_query(self):
        brand_id_s = self.params_storage['brand_id_s']
        self.brand_obj_s = Brand.objects.all()
        for brand_obj in self.brand_obj_s:
            if str(brand_obj.id) in brand_id_s:
                brand_obj.checked = True
        self.brand_maker_id_s = BrandMaker.objects.filter(brand__in=brand_id_s). \
            values_list('id', flat=True)

    def _print_type_s_query(self):
        print_type_id_s = self.params_storage['print_type_id_s']
        self.print_type_obj_s = PrintType.objects.all()
        for print_type_obj in self.print_type_obj_s:
            if str(print_type_obj.id) in print_type_id_s:
                print_type_obj.checked = True
        self.print_type_maker_id_s = PrintTypeMaker.objects.filter(print_type__in=print_type_id_s). \
            values_list('id', flat=True)

    def _set_order_s(self):
        order = self.params_storage['order']
        self.order_s = OrderReference.objects.order_by('-position').all()
        for order_obj in self.order_s:
            order_obj.selected = False
            if order_obj.name == order:
                order_obj.selected = True
        order_selected = OrderReference.objects.get(name=order)
        self.order_name = order_selected.field_name \
            if order_selected.field_order else '-{}'.format(order_selected.field_name)

    def _product_obj_s_query(self):
        self.product_obj_s_query = Product.objects.filter(category_xml__in=self.category_xml_s)

    def _product_filter(self):
        self.product_obj_s_query = Product.objects.filter(category_xml__in=self.category_xml_s)

        filter_s = {
            'brand__in': self.brand_maker_id_s,
            'print_type__in': self.print_type_maker_id_s,

            'price__gte': self.params_storage['price_from'],
            'price__lte': self.params_storage['price_to'],

            'stock__gte': self.params_storage['stock_from'],
            'stock__lte': self.params_storage['stock_to']
        }

        for k, v in filter_s:
            if v:
                self.product_obj_s_query = self.product_obj_s_query.filter(**{k: v})
        self.product_obj_s_query = self.product_obj_s_query.order_by(self.order_name).all()

    def _product_s_query(self):
        paginator = DiggPaginator(self.product_obj_s_query, self.page_size)
        self.page = paginator.page(self.params_storage['page'] or 1)

    def _aggregate(self):
        for item in self.output_context:
            self.output_context[item] = getattr(self, item)

    def get(self, *args, **kwargs):
        self._category_s_query()
        self._brand_s_query()
        self._print_type_s_query()
        self._set_order_s()
        self._product_obj_s_query()
        self._product_filter()
        self._product_s_query()
        self._aggregate()
        return render_to_response(
            self.get_template_name(),
            self.output_context,
            context_instance=RequestContext(self.request), )


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

    request_params_slots = {
        'ajax': [None, 0],
        'product_stock': [None, 0],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'product': None,
            'subproduct_s': None,
            'total_price': None,
            'root_category_s': None,
            'current_category': None,
            'parent_category': None,
            'children_category_s': None,
        }
        super(ProductInsideView, self).__init__(*args, **kwargs)

    def _set_product(self, product_slug_title):
        self.product = get_object_or_404(Product, slug_title=product_slug_title)

    def _category_s_query(self):
        self.root_category_s = CategorySite.get_root_nodes()

        current_categoryxml_s = self.product.category_xml.all()
        if current_categoryxml_s:
            self.current_category = current_categoryxml_s[0].category_site

        self.parent_category = self.current_category.get_parent()

        if not self.parent_category:
            self.parent_category = self.current_category
            self.parent_category.selected = True
        else:
            self.parent_category.selected = False

        self.category_xml_s = list(self.current_category.category_xml_s.all().
                                   values_list('id', flat=True))
        self.children_category_s = self.parent_category.getchildrens()
        for cat in self.children_category_s:
            if self.parent_category.id == self.current_category.id:
                self.category_xml_s.extend(cat.category_xml_s.all().
                                           values_list('id', flat=True))
            cat.selected = True if cat.id == self.current_category.id else False

    def _set_product_params_pack(self):
        self.product.params_pack = []
        for pack_param in self.product.productparamspack_set.filter(pack_id=0).\
                order_by('position').all():
            self.product.params_pack.append({'name': pack_param.name,
                                             'value': pack_param.value,
                                             'position': pack_param.position})

    def _set_product_params_stock(self):
        self.product.params_stock = []
        for stock_param in self.product.productparamsstock_set.order_by('position').all():
            self.product.params_stock.append({'name': stock_param.name,
                                              'value': stock_param.value,
                                              'position': stock_param.position})

    def _set_product_params_other(self):
        self.product.params_other = []
        for other_param in self.product.productparamsother_set.order_by('position').all():
            self.product.params_other.append({'name': other_param.name,
                                              'value': other_param.value,
                                              'position': other_param.position})

    def _set_product_image(self):
        self.product.image_current = self.product.super_big_image or self.product.big_image \
                      or self.product.small_image

    def _set_product_attach_image_s(self):
        self.product.attach_images = self.product.productattachment_set.filter(meaning=1)

    def _set_product_attach_file_s(self):
        self.product.attach_files = self.product.productattachment_set.filter(meaning=0)

    def _set_subproduct_s(self):
        self.subproduct_s = SubProduct.objects.filter(product=self.product)
        for sp in self.subproduct_s:
            sp.params_stock = []
            for stock_param in sp.subproductparamsstock_set.order_by('position').all():
                sp.params_stock.append({'name': stock_param.name,
                                        'value': stock_param.value,
                                        'position': stock_param.position})
            sp.params_other = []
            for other_param in sp.subproductparamsother_set.order_by('position').all():
                sp.params_other.append({'name': other_param.name,
                                        'value': other_param.value,
                                        'position': other_param.position})

    def _get_amount(self):
        self.total_price = 0

    def get(self, *args, **kwargs):
        self._set_product(self.kwargs['product_slug_title'])
        self._category_s_query()
        self._set_product_params_pack()
        self._set_product_params_stock()
        self._set_product_params_other()
        self._set_product_image()
        self._set_product_attach_image_s()
        self._set_product_attach_file_s()
        self._set_subproduct_s()
        self._get_amount()
        self._aggregate()

        if not self.params_storage['ajax']:
            return render_to_response(
                'shop/blocks/catalog/product_inside_general.html',
                self.output_context,
                context_instance=RequestContext(self.request), )
        else:
            return render_to_response(
                'shop/blocks/catalog/product_inside_ajax.html',
                self.output_context,
                context_instance=RequestContext(self.request), )


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
            if item['product_type'] == 'product':
                product = Product.objects.get(pk=item['pk'])
            else:
                product = SubProduct.objects.get(pk=item['pk'])
            quantity = int(item['stock'])
            total_price += product.price * quantity
        self.total_price = str(abs(total_price))

    def get(self, *args, **kwargs):
        self.calc_update()
        self._aggregate()
        return HttpResponse(json.dumps(self.output_context))


class ProductCartView(CatalogBaseView, CatalogParamsValidatorMixin):

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
    }

    session_params_slots = {
        'cart': [None, None],
    }

    session_save_slots = {
        'cart': 'cart_id'
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
        }
        super(ProductCartView, self).__init__(*args, **kwargs)
        self.item_s = None
        self.cart = None
        self.cart_id = None

    def cart_add_item(self):
        self.item_s = json.loads(self.params_storage['item_s'])
        self.cart = Cart(self.params_storage['cart'])
        self.cart_id = self.cart.id
        for item in self.item_s:
            if item['product_type'] == 'product':
                product = Product.objects.get(pk=item['pk'])
            else:
                product = SubProduct.objects.get(pk=item['pk'])
            quantity = int(item['stock'])
            if quantity:
                self.cart.add(product, quantity, None)

    def get(self, *args, **kwargs):
        self.cart_add_item()
        self._save_cookies()
        self._aggregate()
        return HttpResponse(json.dumps(self.output_context))
