# -*- coding: utf-8 -*-


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class CategorySiteListFilter(admin.SimpleListFilter):

    """
    Все подробности в документации - класс фильтр
    для проверки приязки к категории на сайте
    """

    title = 'Категория на сайте'
    parameter_name = 'category_site'

    def lookups(self, request, model_admin):

        return (
            ('Yes', 'Да'),
            ('No', 'Нет'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'Yes':
            return queryset.filter(category_site__isnull=False)
        if self.value() == 'No':
            return queryset.filter(category_site__isnull=True)


class CategoryXMLListFilter(admin.SimpleListFilter):
    """
    Все подробности в документации - класс фильтр
    для проверки приязки к категории на сайте
    """

    title = 'Категория поставщика'
    parameter_name = 'category_xml'

    def lookups(self, request, model_admin):

        return (
            ('Yes', 'Да'),
            ('No', 'Нет'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'Yes':
            return queryset.filter(category_xml__isnull=False)
        if self.value() == 'No':
            return queryset.filter(category_xml__isnull=True)


class BrandListFilter(admin.SimpleListFilter):
    """
    Все подробности в документации - класс фильтр
    для проверки приязки к категории на сайте
    """

    title = 'Бренд на сайте'
    parameter_name = 'brand'

    def lookups(self, request, model_admin):

        return (
            ('Yes', 'Да'),
            ('No', 'Нет'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'Yes':
            return queryset.filter(brand__isnull=False)
        if self.value() == 'No':
            return queryset.filter(brand__isnull=True)


class BrandMakerListFilter(admin.SimpleListFilter):
    """
    Все подробности в документации - класс фильтр
    для проверки приязки к категории на сайте
    """

    title = 'Бренд от поставщика'
    parameter_name = 'brand'

    def lookups(self, request, model_admin):

        return (
            ('Yes', 'Да'),
            ('No', 'Нет'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'Yes':
            return queryset.filter(brand__isnull=False)
        if self.value() == 'No':
            return queryset.filter(brand__isnull=True)


class PrintTypeListFilter(admin.SimpleListFilter):
    """
    Все подробности в документации - класс фильтр
    для проверки приязки к категории на сайте
    """

    title = 'Виды нанесения на сайте'
    parameter_name = 'print_type'

    def lookups(self, request, model_admin):

        return (
            ('Yes', 'Да'),
            ('No', 'Нет'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'Yes':
            return queryset.filter(print_type__isnull=False)
        if self.value() == 'No':
            return queryset.filter(print_type__isnull=True)


class PrintTypeMakerListFilter(admin.SimpleListFilter):
    """
    Все подробности в документации - класс фильтр
    для проверки приязки к категории на сайте
    """

    title = 'Виды нанесения от поставщика'
    parameter_name = 'print_type'

    def lookups(self, request, model_admin):

        return (
            ('Yes', 'Да'),
            ('No', 'Нет'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'Yes':
            return queryset.filter(print_type__isnull=False)
        if self.value() == 'No':
            return queryset.filter(print_type__isnull=True)
