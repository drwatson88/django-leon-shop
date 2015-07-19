# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from models import Category, Tovar, MSettings


def category_list(request):
    categorys = Category.get_root_nodes().filter(show=True)
    # msettings = MSettings.objects.filter(id=1)
    return render_to_response(
        'catalog/tmp.html',
        {
            'categorys': categorys,
            }, context_instance=RequestContext(request), )
