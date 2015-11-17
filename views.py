# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

# from .utils import get_tovars_without_filters

from django.views.generic import ListView
from django.views.generic.edit import FormMixin, ContextMixin

from utils.Pagination import PageRange

from models import Category, Tovar, SubTovar, Stock, Maker
from forms import TovarFormFilter



# def category_list(request):
#     categorys = Category.get_root_nodes().filter(show=True)
#     # msettings = MSettings.objects.filter(id=1)
#     return render_to_response(
#         'catalog/tmp.html',
#         {
#             'categorys': categorys,
#             }, context_instance=RequestContext(request), )


# def category_inside(request, category_uri):
#
#     get_tovars_without_filters(category_uri)
#     return render_to_response('catalog/category_inside.html',
#     {
#         'tovars': tovars,
#     }, context_instance=RequestContext(request), )


def catalog_main(request):

    p = 0
    k = 6
    categorys = list()
    categorys_queue = Category.get_root_nodes().filter(show=True)

    while p < len(categorys_queue):
        categorys.append(categorys_queue[p:p+k])
        p = p + k

    return render_to_response(
        u'catalog/catalog_main.html',
        {
            u'categorys': categorys

            }, context_instance=RequestContext(request), )


class CatalogView(FormMixin, ListView):

    form_class = TovarFormFilter
    template_name = u'catalog/catalog_inside.html'
    context_object_name = u'obj_list'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        cd = super(CatalogView, self).get_context_data(**kwargs)
        cd[u'page_range'] = PageRange(
            cd[u'page_obj'].number,
            cd[u'page_obj'].paginator.num_pages,
            3, 3, 3)
        # cd['query'] = self.get_query(self.form)
        cd[u'form'] = self.form
        cd[u'categorys'] = self.categorys
        cd[u'parent_category'] = self.parent_category
        cd[u'childrens_categorys'] = self.childrens_categorys
        cd[u'current_category'] = self.current_category
        return cd

    # def get_query(self, form):
    #     """
    #     Returns the query provided by the user.
    #     Returns an empty string if the query is invalid.
    #     """
    #     if form.is_valid():
    #         return form.cleaned_data['q']
    #     return ''

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super(CatalogView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super(CatalogView, self).get(request, *args, **kwargs)

    def get_queryset(self):

        self.form.fields[u'makers'].choices = \
            [(x.id, x) for x in Maker.objects.all()]

        catalog_id = self.kwargs[u'catalog_id']
        self.categorys = Category.get_root_nodes()
        self.current_category = Category.objects.filter(id=catalog_id)[0]

        #TODO: сделать обработку исключения и выход на 404 при отсутсвии категории
        self.parent_category = self.current_category.get_parent()
        if not self.parent_category:
            self.parent_category = self.current_category
            self.parent_category.selected = True
        else:
            self.parent_category.selected = False

        categorys_xml = list(self.current_category.categorys_xml.all().values_list(u'id'))
        self.childrens_categorys = self.parent_category.getchildrens()
        for cat in self.childrens_categorys:
            if self.parent_category.id == self.current_category.id:
                categorys_xml.extend(cat.categorys_xml.all().values_list(u'id'))
            cat.selected = True if cat.id == self.current_category.id else False

        tovars = Tovar.objects.filter(categoryxml__in=categorys_xml)
        form_lst = [u'makers', u'price_fr', u'price_to']

        fpage = True
        post = True if self.request.method==u'POST' else False
        for p in form_lst:
            try:
                obj_numb = self.request.POST.get(p, u'')
                print p, obj_numb
                if p == u'makers' and post:
                    post_makers = self.request.POST.getlist(p, u'')
                    makers = Maker.objects.filter(id__in=post_makers)
                    tovars = tovars.filter(maker__in=makers)
                    CatalogView.paginate_by = 1000
                    fpage = False
                elif p == u'price_fr' and obj_numb and post:
                    # obj = CatalogView.objects.get(id=int(obj_numb))
                    tovars = tovars.filter(price__gte=obj_numb)
                    CatalogView.paginate_by = 1000
                    fpage = False
                elif p == u'price_to' and obj_numb and post:
                    tovars = tovars.filter(price__lte=obj_numb)
                    CatalogView.paginate_by = 1000
                    fpage = False
            except:
                pass
        if fpage:
            CatalogView.paginate_by = 30
        return tovars.order_by(u'-id')


def tovar_inside(request, *args, **kwargs):

    catalog_id = kwargs[u'catalog_id']
    tovar_id = kwargs[u'tovar_id']

    """
    По товарам работа
    """
    tovar = Tovar.objects.get(id=tovar_id)

    stock_current = tovar.stock.all()
    tovar.stock_current = stock_current[0] if stock_current else stock_current

    pack_current = tovar.pack_set.all()
    tovar.pack_current = pack_current[0] if pack_current else pack_current

    tovar.image_current = tovar.super_big_image or tovar.big_image or tovar.small_image
    tovar.attach_images = tovar.tovarattachment_set.filter(meaning=1)
    tovar.attach_files = tovar.tovarattachment_set.filter(meaning=0)

    subtovars = SubTovar.objects.filter(tovar=tovar)
    for subtovar in subtovars:
        stock_current = subtovar.stock.all()
        subtovar.stock_current = stock_current[0] if stock_current else stock_current

    """
    По категориям работа для sidebara
    """
    categorys = Category.get_root_nodes()
    current_category = Category.objects.filter(id=catalog_id)[0]

    #TODO: сделать обработку исключения и выход на 404 при отсутсвии категории
    parent_category = current_category.get_parent()
    if not parent_category:
        parent_category = current_category
        parent_category.selected = True
    else:
        parent_category.selected = False

    categorys_xml = list(parent_category.categorys_xml.all().values_list(u'id'))
    childrens_categorys = parent_category.getchildrens()
    for cat in childrens_categorys:
        categorys_xml.extend(cat.categorys_xml.all().values_list(u'id'))
        cat.selected = True if cat.id == current_category.id else False

    return render_to_response(
        u'catalog/tovar_inside.html',
        {
            u'categorys': categorys,
            u'parent_category': parent_category,
            u'childrens_categorys': childrens_categorys,

            u'tovar': tovar,
            u'subtovars': subtovars,

            }, context_instance=RequestContext(request), )


def tovar_nocat_inside(request, *args, **kwargs):

    tovar_id = kwargs[u'tovar_id']

    """
    По товарам работа
    """
    tovar = Tovar.objects.get(id=tovar_id)

    stock_current = tovar.stock.all()
    tovar.stock_current = stock_current[0] if stock_current else stock_current

    pack_current = tovar.pack_set.all()
    tovar.pack_current = pack_current[0] if pack_current else pack_current

    tovar.image_current = tovar.super_big_image or tovar.big_image or tovar.small_image
    tovar.attach_images = tovar.tovarattachment_set.filter(meaning=1)
    tovar.attach_files = tovar.tovarattachment_set.filter(meaning=0)

    subtovars = SubTovar.objects.filter(tovar=tovar)
    for subtovar in subtovars:
        stock_current = subtovar.stock.all()
        subtovar.stock_current = stock_current[0] if stock_current else stock_current

    return render_to_response(
        u'catalog/tovar_nocat_inside.html',
        {
            u'tovar': tovar,
            u'subtovars': subtovars,

            }, context_instance=RequestContext(request), )