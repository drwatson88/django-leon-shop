# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from catalog.views import ProductListView, ProductInsideView, \
    ProductCalcView, ProductCartView, CategoryListView


# TODO: добавиь переход к старым урлам
urlpatterns = patterns(
    'catalog.views',

    url(r'category/$', CategoryListView.as_view(), name='category_list'),
    url(r'category/(?P<catalog_slug_title>.*)/$', ProductListView.as_view(), name='product_list'),
    url(r'product/calc/$', ProductCalcView.as_view(), name='product_calc'),
    url(r'product/cart/$', ProductCartView.as_view(), name='product_cart'),
    url(r'product/(?P<product_slug_title>.*)/$', ProductInsideView.as_view(), name='product_inside'),

    # url(r'(?P<catalog_slug_title>.*)/$', 'product_list', name='product_list'),
    # url(r'$', 'category_list', name='category_list'),
    # url(r'', 'product_inside', name='product_inside'),
)
    # url(r'$', 'cap', name='cap'),)
