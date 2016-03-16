# -*- coding: utf-8 -*-

from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .admin_filters import CategorySiteListFilter, CategoryXMLListFilter, \
    BrandListFilter, BrandMakerListFilter, PrintTypeListFilter, \
    PrintTypeMakerListFilter
from .admin_actions import product_add_category_xml, product_add_print_type, \
    product_clear_category_xmls, product_clear_print_types, product_add_brand, \
    product_add_maker, product_add_status, product_clear_brand, product_clear_maker, \
    product_clear_status, brand_maker_add_brand, brand_maker_clear_brand, \
    print_type_maker_add_print_type, print_type_maker_clear_print_type, \
    category_xml_add_category_site, category_xml_add_maker, category_xml_clear_category_site
from .models import CategorySite, CategoryXML, SubProduct, Product, Status, \
    PrintTypeMaker, PrintType, ProductAttachment, Maker, Brand, BrandMaker


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
    list_display = ('title', 'maker', 'brand')
    fields = ('title', 'maker', 'brand',)
    list_filter = ('maker', BrandListFilter)
    search_fields = ('title',)
    actions = [brand_maker_add_brand, brand_maker_clear_brand]

admin.site.register(BrandMaker, BrandMakerAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('official',)
    search_fields = ('official',)
    fields = ('official',)

admin.site.register(Brand, BrandAdmin)


class CategoryXMLAdmin(TreeAdmin):
    list_display = ('title', 'maker', 'category')
    list_filter = ('status', 'maker', CategorySiteListFilter,)
    search_fields = ('title',)
    actions = [category_xml_add_category_site, category_xml_clear_category_site]

    form = movenodeform_factory(CategorySite, exclude=('cat_id',
                                                       'import_fl',))

admin.site.register(CategoryXML, CategoryXMLAdmin)


class CategorySiteAdmin(TreeAdmin):

    list_display = ('title', 'icon', 'show', )
    list_filter = ('show', )
    search_fields = ('title',)

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
        except BaseException as exc:
            return '<img src="" border="0" alt="" width="60" height="60" align="center" />'

    icon.short_description = 'Миниатюра'
    icon.allow_tags = True
    icon.admin_order_field = 'title'
    prepopulated_fields = {'slug_title': ('title', )}
    # filter_horizontal = ('themes',)

    form = movenodeform_factory(CategorySite)

admin.site.register(CategorySite, CategorySiteAdmin)


class SubProductInline(admin.StackedInline):
    model = SubProduct
    fields = ('product', 'title', 'params', 'stock', 'price')
    extra = 1


class ProductAttachmentInline(admin.StackedInline):
    model = ProductAttachment
    fields = ('product', 'title', 'meaning', 'image', 'file')
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'maker', 'icon', 'show',)
    list_filter = ('show', 'status', 'maker',
                   CategoryXMLListFilter,
                   BrandMakerListFilter,
                   PrintTypeMakerListFilter)
    search_fields = ('title', 'content', 'code',)
    actions = [product_add_category_xml, product_add_print_type,
               product_add_brand, product_add_status, product_add_maker,
               product_clear_category_xmls, product_clear_print_types,
               product_clear_brand, product_clear_status, product_clear_maker,
               ]
    exclude = ('product_id', 'import_fl',)
    # list_editable = ('position',)
    filter_horizontal = ('category_xml', 'print_type')
    inlines = [
        ProductAttachmentInline, SubProductInline
    ]

    def icon(self, obj):

        if obj.small_image:
            from sorl.thumbnail import get_thumbnail

            try:
                im = get_thumbnail(obj.small_image, '60x60', crop='center', quality=99)
                return '<img src="{}" border="0" alt=""  align="center" />'.format(im.url, obj.name)
            except BaseException as exc:
                return '<img src="" border="0" alt="" width="60" height="60" align="center" />'

    icon.short_description = 'Миниатюра'
    icon.allow_tags = True
    icon.admin_order_field = 'title'
    prepopulated_fields = {'code': ('title',),
                           'slug_title': ('title',)}

    class Media:

        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

admin.site.register(Product, ProductAdmin)


class PrintTypeAdmin(admin.ModelAdmin):
    list_display = ('official',)
    search_fields = ('official',)
    fields = ('official',)

admin.site.register(PrintType, PrintTypeAdmin)


class PrintTypeMakerAdmin(admin.ModelAdmin):
    list_display = ('title', 'maker', 'print_type')
    fields = ('title', 'maker', 'print_type',)
    list_filter = ('maker', PrintTypeListFilter)
    search_fields = ('title',)
    actions = [print_type_maker_add_print_type,
               print_type_maker_clear_print_type]

admin.site.register(PrintTypeMaker, PrintTypeMakerAdmin)
