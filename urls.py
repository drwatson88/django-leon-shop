# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import CatalogView

urlpatterns = patterns(
    'catalog.views',
    # url(r'slash/$', 'slash', name = 'slash'),
    url(r'(?P<catalog_id>.*)/(?P<tovar_id>.*)/$', 'tovar_inside', name='tovar_inside'),
    # url(r'(.*)/$', 'category_inside', name='catalog_inside'),
    # url(r'$', 'category_list', name='catalog_list'), )
    url(r'(?P<catalog_id>.*)/$', CatalogView.as_view(), name='catalog_inside'),
    url(r'$', 'catalog_main', name='catalog_main'),)
    # url(r'(?P<p_catalog_id>.*)/(?P<catalog_id>.*)/$', CatalogView.as_view(), name=u'subcatalog_inside'))