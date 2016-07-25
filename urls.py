# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from catalog.views import ProductListView, ProductInsideView, category_list


# TODO: добавиь переход к старым урлам
urlpatterns = patterns(
    'catalog.views',
    # url(r'slash/$', 'slash', name = 'slash'),
    # url(r'^tovar/(?P<tovar_slug_title>.*)/$', 'tovar_inside', name='tovar_inside'),
    # url(r'(?P<catalog_slug_title>.*)/$', CatalogView.as_view(), name='catalog_inside'),

    url(r'category/$', category_list, name='category_list'),
    url(r'category/(?P<catalog_slug_title>.*)/$', ProductListView.as_view(), name='product_list'),
    url(r'product/(?P<product_slug_title>.*)/$', ProductInsideView.as_view(), name='product_inside'),

    # url(r'(?P<catalog_slug_title>.*)/$', 'product_list', name='product_list'),
    # url(r'$', 'category_list', name='category_list'),
    # url(r'', 'product_inside', name='product_inside'),
)
    # url(r'$', 'cap', name='cap'),)
