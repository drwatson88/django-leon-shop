# -*- coding: utf-8 -*-

from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from models import Category, CategoryXML, SubTovar, Tovar, Status, Pack, Group, \
    FilterType, Filter, PrintType, TovarAttachment



class StatusAdmin(admin.ModelAdmin):

    pass

admin.site.register(Status, StatusAdmin)


class CategoryXMLAdmin(TreeAdmin):

    pass

admin.site.register(CategoryXML, CategoryXMLAdmin)


class CategoryAdmin(TreeAdmin):

    form = movenodeform_factory(Category)

admin.site.register(Category, CategoryAdmin)


class TovarAdmin(admin.ModelAdmin):

    pass

admin.site.register(Tovar, TovarAdmin)


class SubTovarAdmin(admin.ModelAdmin):

    pass

admin.site.register(SubTovar, SubTovarAdmin)


class PackAdmin(admin.ModelAdmin):

    pass

admin.site.register(Pack, PackAdmin)


class FilterTypeAdmin(admin.ModelAdmin):

    pass

admin.site.register(FilterType, FilterTypeAdmin)


class FilterAdmin(admin.ModelAdmin):

    pass

admin.site.register(Filter, FilterAdmin)


class PrintTypeAdmin(admin.ModelAdmin):

    pass

admin.site.register(PrintType, PrintTypeAdmin)


class TovarAttachmentAdmin(admin.ModelAdmin):

    pass

admin.site.register(TovarAttachment, TovarAttachmentAdmin)