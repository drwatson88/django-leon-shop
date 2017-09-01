# coding: utf-8

from django.conf.urls import patterns, url
from .views import CartList, CartCalc, CartMenu


urlpatterns = patterns('basket.views',
                       url(r'^list', CartList.as_view(), name='list'))
