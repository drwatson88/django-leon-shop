# -*- coding: utf-8 -*-


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class DecadeBornListFilter(admin.SimpleListFilter):

    """
    Все подробности в документации - класс фильтр
    для проверки приязки к категории на сайте
    """

    title = 'Категория на сайте'
    parameter_name = 'category'

    def lookups(self, request, model_admin):

        return (
            ('Yes', 'Да'),
            ('No', 'Нет'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'Yes':
            return queryset.filter(category__isnull=False)
        if self.value() == 'No':
            return queryset.filter(category__isnull=True)