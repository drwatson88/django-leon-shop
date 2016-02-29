# -*- coding: utf-8 -*-

from django.contrib import admin

from admin_filters import CategoryListFilter, CategoryXMLListFilter
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from settings import MEDIA_URL
from models import Category, CategoryXML, SubTovar, Tovar, Status, \
    PrintType, TovarAttachment, Maker, Brand


class StatusAdmin(admin.ModelAdmin):

    pass

admin.site.register(Status, StatusAdmin)


class MakerAdmin(admin.ModelAdmin):

    pass

admin.site.register(Maker, MakerAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('maker', 'name',)


admin.site.register(Brand, MakerAdmin)


class CategoryXMLAdmin(TreeAdmin):
    list_display = ('name', 'maker', 'category')
    list_filter = ('status', 'maker', CategoryListFilter,)
    search_fields = ('name',)

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

    list_display = ('name', 'icon', 'show', )
    list_filter = ('show', 'status', 'maker', CategoryXMLListFilter)
    search_fields = ('name', 'content', 'code',)
    exclude = ('product_id', 'import_fl',)
    # list_editable = ('position',)
    filter_horizontal = ('categoryxml', 'print_type')
    inlines = [
        TovarAttachmentInline, SubTovarInline
    ]

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'categoryxml':
            kwargs['queryset'] = CategoryXML.objects.filter(maker=request.maker)
        return super(TovarAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

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

    pass

admin.site.register(PrintType, PrintTypeAdmin)
