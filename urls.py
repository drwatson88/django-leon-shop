# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import CatalogView

urlpatterns = patterns(
    'catalog.views',
    # url(r'slash/$', 'slash', name = 'slash'),
    url(r'^tovar/(?P<tovar_slug_title>.*)/$', 'tovar_inside', name='tovar_inside'),
    url(r'(?P<catalog_slug_title>.*)/$', CatalogView.as_view(), name='catalog_inside'),
    url(r'$', 'catalog_main', name='catalog_main'),)