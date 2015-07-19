#-*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'catalog.views',
    # url(r'slash/$', 'slash', name = 'slash'),
    # url(r'(.*)/(.*)/$', 'tovar_inside', name='tovar_inside'),
    # url(r'(.*)/$', 'category_inside', name='catalog_inside'),
    url(r'$', 'category_list', name='catalog_list'), )