# -*- coding: utf-8 -*-

from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .admin_filters import CategoryListFilter, CategoryXMLListFilter, \
    BrandListFilter, BrandMakerListFilter, PrintTypeListFilter, \
    PrintTypeMakerListFilter
from .admin_actions import tovar_add_categoryxml, tovar_add_print_type, \
    tovar_clear_categoryxmls, tovar_clear_print_types, tovar_add_brand, \
    tovar_add_maker, tovar_add_status, tovar_clear_brand, tovar_clear_maker, \
    tovar_clear_status, brand_maker_add_brand, brand_maker_clear_brand, \
    print_type_maker_add_print_type, print_type_maker_clear_print_type, \
    categoryxml_add_category, categoryxml_add_maker, categoryxml_clear_category
from .models import Category, CategoryXML, SubTovar, Tovar, Status, \
    PrintTypeMaker, PrintType, TovarAttachment, Maker, Brand, BrandMaker


class StatusAdmin(admin.ModelAdmin):
    list_display = ('official',)
    search_fields = ('official',)
    fields = ('official',)

admin.site.register(Status, StatusAdmin)


class MakerAdmin(admin.ModelAdmin):
    list_display = ('official',)
    search_fields = ('official',)
    fields = ('official',)

admin.site.register(Maker, MakerAdmin)


class BrandMakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'maker', 'brand')
    fields = ('name', 'maker', 'brand',)
    list_filter = ('maker', BrandListFilter)
    search_fields = ('name',)
    actions = [brand_maker_add_brand, brand_maker_clear_brand]

admin.site.register(BrandMaker, BrandMakerAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('official',)
    search_fields = ('official',)
    fields = ('official',)

admin.site.register(Brand, BrandAdmin)


class CategoryXMLAdmin(TreeAdmin):
    list_display = ('name', 'maker', 'category')
    list_filter = ('status', 'maker', CategoryListFilter,)
    search_fields = ('name',)
    actions = [categoryxml_add_category, categoryxml_clear_category]

    form = movenodeform_factory(Category, exclude=('cat_id',
                                                   'import_fl',))

admin.site.register(CategoryXML, CategoryXMLAdmin)


class CategoryAdmin(TreeAdmin):

    list_display = ('name', 'icon', 'show', )
    list_filter = ('show', )
    search_fields = ('name',)

    class Media:

        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

    def icon(self, obj):
        from sorl.thumbnail import get_thumbnail

        try:
            im = get_thumbnail(obj.image, '60x60', crop='center', quality=99)
            return '<img src="{}" border="0" alt=""  align="center" />'.format(im.url)
        except:
            return '<img src="{}" border="0" alt="" width="60" height="60" align="center" />'.\
                format('')

    icon.short_description = 'Миниатюра'
    icon.allow_tags = True
    icon.admin_order_field = 'name'
    prepopulated_fields = {'slug_title': ('name', )}
    # filter_horizontal = ('themes',)

    form = movenodeform_factory(Category)

admin.site.register(Category, CategoryAdmin)


class SubTovarInline(admin.StackedInline):
    model = SubTovar
    fields = ('tovar', 'name', 'params', 'stock', 'price')
    extra = 1


class TovarAttachmentInline(admin.StackedInline):
    model = TovarAttachment
    fields = ('tovar', 'name', 'meaning', 'image', 'file')
    extra = 1


class TovarAdmin(admin.ModelAdmin):
    list_display = ('name', 'maker', 'icon', 'show',)
    list_filter = ('show', 'status', 'maker',
                   CategoryXMLListFilter,
                   BrandMakerListFilter,
                   PrintTypeMakerListFilter)
    search_fields = ('name', 'content', 'code',)
    actions = [tovar_add_categoryxml, tovar_add_print_type,
               tovar_add_brand, tovar_add_status, tovar_add_maker,
               tovar_clear_categoryxmls, tovar_clear_print_types,
               tovar_clear_brand, tovar_clear_status, tovar_clear_maker,
               ]
    exclude = ('product_id', 'import_fl',)
    # list_editable = ('position',)
    filter_horizontal = ('categoryxml', 'print_type')
    inlines = [
        TovarAttachmentInline, SubTovarInline
    ]

    def icon(self, obj):

        if obj.small_image:
            from sorl.thumbnail import get_thumbnail

            try:
                im = get_thumbnail(obj.small_image, '60x60', crop='center', quality=99)
                return '<img src="{}" border="0" alt=""  align="center" />'.format(im.url, obj.name)
            except:
                return '<img src="" border="0" alt="" width="60" height="60" align="center" />'

    icon.short_description = 'Миниатюра'
    icon.allow_tags = True
    icon.admin_order_field = 'name'
    prepopulated_fields = {'code': ('name',),
                           'slug_title': ('name',)}

    class Media:

        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

admin.site.register(Tovar, TovarAdmin)


class PrintTypeAdmin(admin.ModelAdmin):
    list_display = ('official',)
    search_fields = ('official',)
    fields = ('official',)

admin.site.register(PrintType, PrintTypeAdmin)


class PrintTypeMakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'maker', 'print_type')
    fields = ('name', 'maker', 'print_type',)
    list_filter = ('maker', PrintTypeListFilter)
    search_fields = ('name',)
    actions = [print_type_maker_add_print_type,
               print_type_maker_clear_print_type]

admin.site.register(PrintTypeMaker, PrintTypeMakerAdmin)
