#-*- coding: utf-8 -*-

from .models import CategorySite


def categorys(request):

    try:
        return {'catalog': CategorySite.get_root_nodes()[0].get_children().filter(show=True)}
    except Exception:
        return {'catalog': []}