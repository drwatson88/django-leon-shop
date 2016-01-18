# -*- coding: utf-8 -*-

from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from models import Category, CategoryXML, SubTovar, Tovar, Status, \
                    PrintType, TovarAttachment, Maker


class StatusAdmin(admin.ModelAdmin):

    pass

admin.site.register(Status, StatusAdmin)


class MakerAdmin(admin.ModelAdmin):

    pass

admin.site.register(Maker, MakerAdmin)


class CategoryXMLAdmin(TreeAdmin):

    form = movenodeform_factory(Category)

admin.site.register(CategoryXML, CategoryXMLAdmin)


class CategoryAdmin(TreeAdmin):

    list_display = ('name', 'icon', 'show', )
    list_filter = ('show', )
    search_fields = ('name',)

    # class Media:
    #   js = [
    #     '/media/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
    #     '/media/grappelli/tinymce_setup/tinymce_setup.js',
    #   ]

    def icon(self, obj):
        from sorl.thumbnail import get_thumbnail

        try:
            im = get_thumbnail(obj.image, '60x60', crop='center', quality=99)
            return '<img src="{}" border="0" alt=""  align="center" />'.format(im.url)
        except:
            return '<img src="{}" border="0" alt="" width="60" height="60" align="center" />'.format('')

    icon.short_description = 'Миниатюра'
    icon.allow_tags = True
    icon.admin_order_field = 'name'
    prepopulated_fields = {'slug_title': ('name', )}
    # filter_horizontal = ('themes',)

    form = movenodeform_factory(Category)

admin.site.register(Category, CategoryAdmin)


class TovarAdmin(admin.ModelAdmin):

    pass


class SubTovarAdmin(admin.ModelAdmin):

    pass

admin.site.register(SubTovar, SubTovarAdmin)


class PrintTypeAdmin(admin.ModelAdmin):

    pass

admin.site.register(PrintType, PrintTypeAdmin)


class TovarAttachmentAdmin(admin.ModelAdmin):

    pass

admin.site.register(TovarAttachment, TovarAttachmentAdmin)