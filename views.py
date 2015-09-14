# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

# from .utils import get_tovars_without_filters

from django.views.generic import ListView
from django.views.generic.edit import FormMixin, ContextMixin

from utils.Pagination import PageRange

from models import Category, Tovar, Maker
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
    categorys = Category.get_root_nodes().filter(show=True)
    return render_to_response(
        u'catalog/catalog_main.html',
        {
            u'categorys': categorys

            }, context_instance=RequestContext(request), )


# class CatalogView(ContextMixin, FormMixin, ListView):
class CatalogView(FormMixin, ListView):

    form_class = TovarFormFilter
    template_name = u'catalog/catalog_inside.html'
    context_object_name = u'obj'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        cd = super(CatalogView, self).get_context_data(**kwargs)
        cd[u'page_range'] = PageRange(
            cd[u'page_obj'].number,
            cd[u'page_obj'].paginator.num_pages,
            3, 3, 3)
        # cd['query'] = self.get_query(self.form)
        cd[u'form'] = self.form
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
        catalog_id = self.kwargs[u'catalog_id']
        category = Category.objects.filter(id=catalog_id)[0]
        categorys_xml = list(category.categorys_xml.all().values_list(u'id'))
        tovars = Tovar.objects.filter(categoryxml__in=categorys_xml)
        print tovars

        form_lst = [u'maker', u'price_fr', u'price_to']

        fpage = True
        for p in form_lst:
            try:
                obj_numb = self.request.POST.get(p, u'')
                # print p, obj_numb
                if p == u'maker' and obj_numb:
                    obj = Maker.objects.get(id=int(obj_numb))
                    tovars = tovars.filter(maker=obj)
                    CatalogView.paginate_by = 1000
                    fpage = False
                elif p == u'price_fr' and obj_numb:
                    # obj = CatalogView.objects.get(id=int(obj_numb))
                    tovars = tovars.filter(price__gte=obj_numb)
                    CatalogView.paginate_by = 1000
                    fpage = False
                elif p == u'price_to' and obj_numb:
                    tovars = tovars.filter(price__lte=obj_numb)
                    CatalogView.paginate_by = 1000
                    fpage = False
            except:
                pass
        if fpage:
            CatalogView.paginate_by = 30
        return tovars.order_by(u'-id')





    # template_name
    #
    # def get(self, request, *args, **kwargs):
    #
    #     print args, kwargs
    #     # Tovars=Tovar.objects.filter(category)
    #     return render_to_response(
    #         'catalog/tmp2.html',
    #         {
    #             # 'categorys': categorys,
    #             }, context_instance=RequestContext(request), )
    #
    # def post(self):
    #     pass
