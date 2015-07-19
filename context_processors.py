#-*- coding: utf-8 -*-

from models import Category

def categorys(request):
    try:
        return {'catalog': Category.get_root_nodes()[0].get_children().filter(show=True)}
    except Exception:
        return {'catalog': []}