# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, HttpResponse

from .models import CategorySite, Product, Brand, BrandMaker
from .base import CatalogBaseView, ParamsValidatorMixin


PAGE_STEP = 10
PAGE_SIZE = 20
GRID_COUNT = 4


def category_list(request, ):

    """ View for category list. Delimiter k = 6.

        :param request request input for all views
        :type request object
    """

    category_all = list()
    category_s_queue = CategorySite.get_root_nodes().filter(show=True)

    p = 0
    k = 6
    while p < len(category_s_queue):
        category_all.append(category_s_queue[p:p+k])
        p += k

    return render_to_response(
        'blocks/catalog/category_list.html',
        {
            'category_all': category_all
        },
        context_instance=RequestContext(request), )


def product_list(request, catalog_slug_title):

    """ View for products in category (category maybe not low level,
        in this case products collect in all daughter's category's)
        All category's have two levels.

        :param request Request
        :type request object

        :param catalog_slug_title slug_title - unique key for all category's
        :type catalog_slug_title str
    """

    # Get POST params
    ajax = request.GET.get('ajax', 0)
    grid = request.GET.get('grid', 1)
    grid_cnt = request.GET.get('grid_cnt', GRID_COUNT)
    order_by = request.GET.get('order_by', 'title')
    page_size = request.GET.get('page_size', PAGE_SIZE)
    page_no = request.GET.get('page_no', 1)
    brand_id_s = request.GET.get('brands', [])

    # Validation
    grid_cnt = int(grid_cnt) if grid_cnt in (3, 4) else 4
    page_size = int(page_size) if page_size > 5 else 20
    page_no = int(page_no) if page_no > 0 else 1

    if order_by.strip('-') in ('title', 'price'):
        order_by = order_by
    elif order_by == 'default':
        order_by = 'title'

    brand_id_s = brand_id_s if isinstance(brand_id_s, list) else []

    # Category's query's
    root_category_s = CategorySite.get_root_nodes()
    current_category = CategorySite.objects.filter(slug_title=catalog_slug_title)[0]
    parent_category = current_category.get_parent()

    if not parent_category:
        parent_category = current_category
        parent_category.selected = True
    else:
        parent_category.selected = False

    category_xml_s = list(current_category.category_xml_s.all().values_list('id', flat=True))
    children_category_s = parent_category.getchildrens()
    for cat in children_category_s:
        if parent_category.id == current_category.id:
            category_xml_s.extend(cat.category_xml_s.all().values_list('id', flat=True))
        cat.selected = True if cat.id == current_category.id else False

    # Brands
    brand_obj_s = Brand.objects.all()
    brand_id_s = brand_id_s if brand_id_s else brand_obj_s.values_list('id', flat=True)
    for brand_obj in brand_obj_s:
        if brand_obj.id in brand_id_s:
            brand_obj.checked = True
    brand_maker_id_s = BrandMaker.objects.filter(brand__in=brand_id_s). \
        values_list('id', flat=True)

    # Product's query
    product_obj_s_query = Product.objects.filter(category_xml__in=category_xml_s,
                                                 brand__in=brand_maker_id_s)
    product_obj_s_count = len(product_obj_s_query)
    page_no = page_no if (page_no-1)*page_size < len(product_obj_s_query) else 1
    product_obj_s = product_obj_s_query.order_by(order_by)[(page_no-1)*page_size: page_no*page_size]
    product_s = [product_obj_s[k: k + grid_cnt] for k in range(0, len(product_obj_s)//grid_cnt)]

    # Pages
    page_s = [{'id': k} for k in range((page_no//PAGE_STEP)*PAGE_STEP + 1,
                                       min((page_no//PAGE_STEP + 1)*PAGE_STEP,
                                           product_obj_s_count//page_size + 1) + 1)]
    page_start = (page_no//PAGE_STEP)*PAGE_STEP + 1
    page_stop = (page_no//PAGE_STEP + 1)*PAGE_STEP
    page_count = product_obj_s_count//page_size
    if not ajax:
        return render_to_response(
            'blocks/catalog/product_list_general.html',
            {
                'current_category': current_category,
                'parent_category': parent_category,
                'children_category_s': children_category_s,
                'root_category_s': root_category_s,
                'product_s': product_s,
                'brand_s': brand_obj_s,
                'pages': page_s,
                'page_start': page_start,
                'page_stop': page_stop,
                'page_count': page_count
            },
            context_instance=RequestContext(request), )
    else:
        return render_to_response(
            'blocks/catalog/product_list_ajax.html',
            {
                'current_category': current_category,
                'parent_category': parent_category,
                'children_category_s': children_category_s,
                'root_category_s': root_category_s,
                'product_s': product_s,
                'brand_s': brand_obj_s,
                'pages': {}
            },
            context_instance=RequestContext(request), )


def product_inside(request):

    return render_to_response(
        'blocks/catalog/category_list.html',
        {},
        context_instance=RequestContext(request), )


class ProductListView(CatalogBaseView, ParamsValidatorMixin):

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

    params_slots = {
        'ajax': [None, 0],
        'grid': [None, 1],
        'grid_cnt': [None, GRID_COUNT],
        'order': [None, 'title'],
        'page_no': [None, 1],
        'page_size': [None, 20],
        'brand_id_s': [None, []],
    }

    def __init__(self, *args, **kwargs):
        self.params_storage = {}
        self.output_context = {
            'root_category_s': None,
            'current_category': None,
            'parent_category': None,
            'category_xml_s': None,
            'children_category_s': None,
            'brand_obj_s': None,
            'product_s': None,
            'page_s': None,
            'page_start': None,
            'page_stop': None,
            'page_count': None
        }
        super(ProductListView, self).__init__(*args, **kwargs)

    def _category_s_query(self, catalog_slug_title):
        self.root_category_s = CategorySite.get_root_nodes()
        self.current_category = CategorySite.objects.filter(slug_title=catalog_slug_title)[0]
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
                self.category_xml_s.extend(cat.category_xml_s.all().values_list('id', flat=True))
            cat.selected = True if cat.id == self.current_category.id else False

    def _brand_s_query(self, brand_id_s):
        self.brand_obj_s = Brand.objects.all()
        brand_id_s = brand_id_s if brand_id_s else self.brand_obj_s.values_list('id', flat=True)
        for brand_obj in self.brand_obj_s:
            if brand_obj.id in brand_id_s:
                brand_obj.checked = True
        self.brand_maker_id_s = BrandMaker.objects.filter(brand__in=brand_id_s). \
            values_list('id', flat=True)

    def _product_s_query(self, page_no, page_size, order, grid_cnt):
        product_obj_s_query = Product.objects.filter(category_xml__in=self.category_xml_s,
                                                     brand__in=self.brand_maker_id_s)
        self.product_obj_s_count = len(product_obj_s_query)
        page_no = page_no if (page_no-1)*page_size < len(product_obj_s_query) else 1
        product_obj_s = product_obj_s_query.order_by(order)[(page_no-1)*page_size: page_no*page_size]
        self.product_s = [product_obj_s[k: k + grid_cnt] for k in range(0, len(product_obj_s)//grid_cnt)]

    def _page_s(self, page_no, page_size):
        self.page_s = [
            {
               'id': k, 'active': (True if k == page_no else False)
            } for k in range((page_no//PAGE_STEP)*PAGE_STEP + 1,
                             min((page_no//PAGE_STEP + 1)*PAGE_STEP,
                                 self.product_obj_s_count//page_size + 1) + 1)]
        self.page_start = (page_no//PAGE_STEP)*PAGE_STEP + 1
        self.page_stop = (page_no//PAGE_STEP + 1)*PAGE_STEP
        self.page_count = self.product_obj_s_count//page_size

    def _aggregate(self):
        for item in self.output_context:
            self.output_context[item] = getattr(self, item)

    def get(self, *args, **kwargs):
        self._category_s_query(self.kwargs['catalog_slug_title'])
        self._brand_s_query(self.params_storage['brand_id_s'])
        self._product_s_query(self.params_storage['page_no'], self.params_storage['page_size'],
                              self.params_storage['order'], self.params_storage['grid_cnt'])
        self._page_s(self.params_storage['page_no'],
                     self.params_storage['page_size'])
        self._aggregate()
        if not self.params_storage['ajax']:
            return render_to_response(
                'blocks/catalog/product_list_general.html',
                self.output_context,
                context_instance=RequestContext(self.request), )
        else:
            return render_to_response(
                'blocks/catalog/product_list_ajax.html',
                self.output_context,
                context_instance=RequestContext(self.request), )

