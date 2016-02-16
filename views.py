# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

# from .utils import get_tovars_without_filters

from django.views.generic import ListView
from django.views.generic.edit import FormMixin, ContextMixin
from django.http import Http404

from utils.Pagination import PageRange

from models import Category, Tovar, SubTovar, Maker
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
        'catalog/catalog_main.html',
        {
            'categorys': categorys

            }, context_instance=RequestContext(request), )


class CatalogView(FormMixin, ListView):

    form_class = TovarFormFilter
    template_name = 'catalog/catalog_inside.html'
    context_object_name = 'obj_list'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        cd = super(CatalogView, self).get_context_data(**kwargs)
        cd['page_range'] = PageRange(
            cd['page_obj'].number,
            cd['page_obj'].paginator.num_pages,
            3, 3, 3)
        # cd['query'] = self.get_query(self.form)
        cd['form'] = self.form
        cd['categorys'] = self.categorys
        cd['parent_category'] = self.parent_category
        cd['childrens_categorys'] = self.childrens_categorys
        cd['current_category'] = self.current_category
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

        self.form.fields['makers'].choices = \
            [(x.id, x) for x in Maker.objects.all()]

        catalog_slug_title = self.kwargs['catalog_slug_title']
        self.categorys = Category.get_root_nodes()
        self.current_category = Category.objects.filter(slug_title=
                                                        catalog_slug_title)[0]

        #TODO: сделать обработку исключения и выход на 404 при отсутсвии категории
        self.parent_category = self.current_category.get_parent()
        if not self.parent_category:
            self.parent_category = self.current_category
            self.parent_category.selected = True
        else:
            self.parent_category.selected = False

        categorys_xml = list(self.current_category.categorys_xml.all().
                             values_list('id'))
        self.childrens_categorys = self.parent_category.getchildrens()
        for cat in self.childrens_categorys:
            if self.parent_category.id == self.current_category.id:
                categorys_xml.extend(cat.categorys_xml.all().values_list('id'))
            cat.selected = True if cat.id == self.current_category.id else False

        tovars = Tovar.objects.filter(categoryxml__in=categorys_xml)
        form_lst = ['makers', 'price_fr', 'price_to']

        fpage = True
        post = True if self.request.method == 'POST' else False
        for p in form_lst:
            try:
                obj_numb = self.request.POST.get(p, '')
                if p == 'makers' and post:
                    post_makers = self.request.POST.getlist(p, '')
                    makers = Maker.objects.filter(id__in=post_makers)
                    tovars = tovars.filter(maker__in=makers)
                    CatalogView.paginate_by = 1000
                    fpage = False
                elif p == 'price_fr' and obj_numb and post:
                    # obj = CatalogView.objects.get(id=int(obj_numb))
                    tovars = tovars.filter(price__gte=obj_numb)
                    CatalogView.paginate_by = 1000
                    fpage = False
                elif p == 'price_to' and obj_numb and post:
                    tovars = tovars.filter(price__lte=obj_numb)
                    CatalogView.paginate_by = 1000
                    fpage = False
            except:
                pass
        if fpage:
            CatalogView.paginate_by = 30
        return tovars.order_by('-id')


def tovar_inside(request, *args, **kwargs):

    tovar_slug_title = kwargs['tovar_slug_title']

    """
    Находим главный товар
    """
    try:
        tovar = Tovar.objects.get(slug_title=tovar_slug_title)
    except Tovar.DoesNotExist:
        raise Http404()

    """
    Берем пакет хранения из таблицы доп.параметров пакета
    """
    tovar.pack_current = {}
    for pack_param in tovar.tovarparamspack_set.all()\
            .order_by('position'):
        tovar.pack_current.update({
            pack_param.abbr: [pack_param.name, pack_param.value]
        })

    tovar.other = {}
    for other_param in tovar.tovarparamsother_set.all()\
            .order_by('position'):
        tovar.other.update({
            other_param.abbr: [other_param.name, other_param.value]
        })
    # tovar.matherial = tovar.other['matherial'][1]
    # tovar.weight = tovar.other['weight'][1]
    # tovar.product_size = tovar.other['product_size'][1]

    tovar.image_current = tovar.super_big_image or tovar.big_image \
                          or tovar.small_image
    tovar.attach_images = tovar.tovarattachment_set.filter(meaning=1)
    tovar.attach_files = tovar.tovarattachment_set.filter(meaning=0)

    subtovars = SubTovar.objects.filter(tovar=tovar)
    for subtovar in subtovars:
        subtovar.stock_current = {}
        for stock_param in tovar.tovarparamspack_set.all()\
                .order_by('position'):
            subtovar.stock_current.update({
                stock_param.abbr: [stock_param.name, stock_param.value]
            })

    """
    По категориям работа для sidebara
    """
    categorys_xml = tovar.categoryxml.all()
    path_categorys = [cat_xml.category for cat_xml in categorys_xml
                      if cat_xml.category is not None]
    current_category = path_categorys[0]

    categorys = Category.get_root_nodes()

    #TODO: сделать обработку исключения и выход на 404 при отсутсвии категории
    parent_category = current_category.get_parent()
    if not parent_category:
        parent_category = current_category
        parent_category.selected = True
    else:
        parent_category.selected = False

    childrens_categorys = parent_category.getchildrens()
    for cat in childrens_categorys:
        cat.selected = True if cat.id == current_category.id else False

    return render_to_response(
        'catalog/tovar_inside.html',
        {
            'categorys': categorys,
            'parent_category': parent_category,
            'childrens_categorys': childrens_categorys,
            'current_category': current_category,

            'tovar': tovar,
            'subtovars': subtovars,

            }, context_instance=RequestContext(request), )