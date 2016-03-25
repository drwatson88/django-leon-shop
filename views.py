# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from .models import CategorySite, Product, Brand, BrandMaker


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
    grid = request.GET.get('grid', 1)
    grid_cnt = request.GET.get('grid_cnt', 4)
    order_by = request.GET.get('order_by', 'title')
    page_size = request.GET.get('page_size', 20)
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
    product_obj_s_query = Product.objects.filter(category_xml__in=category_xml_s, brand__in=brand_maker_id_s)
    page_no = page_no if (page_no-1)*page_size < len(product_obj_s_query) else 1
    product_obj_s = product_obj_s_query.order_by(order_by)[(page_no-1)*page_size: page_no*page_size]
    product_s = [product_obj_s[k: k + grid_cnt] for k in range(0, len(product_obj_s)//grid_cnt)]

    return render_to_response(
        'blocks/catalog/product_list.html',
        {
            'current_category': current_category,
            'parent_category': parent_category,
            'children_category_s': children_category_s,

            'product_s': product_s,
            # 'page': page,

            'root_category_s': root_category_s,

            'brand_s': brand_obj_s
        },
        context_instance=RequestContext(request), )


def product_inside(request):

    return render_to_response(
        'blocks/catalog/category_list.html',
        {},
        context_instance=RequestContext(request), )
