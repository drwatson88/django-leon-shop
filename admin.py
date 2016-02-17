# -*- coding: utf-8 -*-

from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from settings import MEDIA_URL
from models import Category, CategoryXML, SubTovar, Tovar, Status, \
                    PrintType, TovarAttachment, Maker


class StatusAdmin(admin.ModelAdmin):

    pass

admin.site.register(Status, StatusAdmin)


class MakerAdmin(admin.ModelAdmin):

    pass

admin.site.register(Maker, MakerAdmin)


class CategoryXMLAdmin(TreeAdmin):
    list_display = ('name', 'maker', 'cat_id', 'category')
    list_filter = ('status', 'maker', )
    search_fields = ('name',)

    form = movenodeform_factory(Category)

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


class TovarAdmin(admin.ModelAdmin):

    list_display = ('name', 'icon', 'show', )
    list_filter = ('show', 'status', 'maker', )
    search_fields = ('name', 'content', 'code',)
    # list_editable = ('position',)
    # filter_horizontal = ('categoryxml',)
    # inlines = [
    #       PhotosInline,VariantsInline,
    # ]

    class Media:

        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

    def icon(self, obj):

        if obj.small_image:
            from sorl.thumbnail import get_thumbnail

            try:
                im = get_thumbnail(obj.small_image, '60x60', crop='center', quality=99)
                return '<img src="{}" border="0" alt=""  align="center" />'.format(im.url, obj.name)
            except :
                return '<img src="" border="0" alt="" width="60" height="60" align="center" />'

    icon.short_description = 'Миниатюра'
    icon.allow_tags = True
    icon.admin_order_field = 'name'
    prepopulated_fields = {'slug_title': ('name', )}

admin.site.register(Tovar, TovarAdmin)


class PrintTypeAdmin(admin.ModelAdmin):

    pass

admin.site.register(PrintType, PrintTypeAdmin)