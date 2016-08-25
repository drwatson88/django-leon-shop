# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django import http

from .models import CategorySiteRedirect, ProductRedirect


def category_site_redirect(request, slug_name):
    try:
        category_site_redirect = CategorySiteRedirect.objects.get(old_slug_name=slug_name)
        if not category_site_redirect.category_site:
            raise http.Http404()
    except ObjectDoesNotExist as exc:
        raise http.Http404()
    finally:
        http.HttpResponseRedirect('/catelog/categorysite/{}'.
                                  format(category_site_redirect.category_site.slug_title))


def product_redirect(request, slug_name):
    try:
        product_redirect = ProductRedirect.objects.get(old_slug_name=slug_name)
        if not product_redirect.product:
            raise http.Http404()
    except ObjectDoesNotExist as exc:
        raise http.Http404()
    finally:
        http.HttpResponseRedirect('/catelog/categorysite/{}'.
                                  format(product_redirect.product.slug_title))
