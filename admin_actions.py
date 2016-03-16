# coding: utf-8


from .admin_forms import ChangeProductCategoryXMLForm, ChangeProductPrintTypeForm, \
    ChangeCategoryXMLCategorySiteForm, ChangeBrandMakerBrandForm, \
    ChangePrintTypeMakerPrintTypeForm, ChangeCategoryXMLMakerForm, \
    ChangeProductBrandForm, ChangeProductMakerForm, ChangeProductStatusForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import admin


def product_add_category_xml(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeProductCategoryXMLForm(request.POST)

        if form.is_valid():
            category_xml = form.cleaned_data['category_xml']

            count = 0
            for item in queryset:
                item.category_xml.add(category_xml)
                item.save()
                count += 1

            modeladmin.message_user(request, 'Категория от поставщика {} '
                                             'применена к {} товарам.'.
                                    format(category_xml, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeProductCategoryXMLForm(initial={'_selected_action': request.
                                          POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/product_add_category_xml.html', {'items': queryset,
                                                                             'form': form,
                                                                             'title': 'Добавление категории '
                                                                                      'от поставщика'})

product_add_category_xml.short_description = 'Добавить КАТЕГОРИЮ ОТ ПОСТАВЩИКА'


def product_clear_category_xmls(modeladmin, request, queryset):
    for item in queryset:
        item.category_xml.clear()

product_clear_category_xmls.short_description = 'Очистить поле КАТЕГОРИИ ОТ ПОСТАВЩИКА'


def product_add_print_type(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeProductPrintTypeForm(request.POST)

        if form.is_valid():
            print_type = form.cleaned_data['print_type']

            count = 0
            for item in queryset:
                item.print_type.add(print_type)
                item.save()
                count += 1

            modeladmin.message_user(request, 'Вид нанесения от поставщика {} '
                                             'применен к {} товарам.'.
                                    format(print_type, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeProductPrintTypeForm(initial={'_selected_action': request.
                                        POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/product_add_print_type.html', {'items': queryset,
                                                                           'form': form,
                                                                           'title': 'Добавить вид нанесения '
                                                                                    'от поставщика'})

product_add_print_type.short_description = 'Добавить ВИД НАНЕСЕНИЯ ОТ ПОСТАВЩИКА'


def product_clear_print_types(modeladmin, request, queryset):
    for item in queryset:
        item.print_type.clear()

product_clear_print_types.short_description = 'Очистить поле ВИДЫ НАНЕСЕНИЯ ОТ ПОСТАВЩИКА'


def product_add_brand(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeProductBrandForm(request.POST)

        if form.is_valid():
            brand = form.cleaned_data['brand']

            count = 0
            for item in queryset:
                item.brand = brand
                item.save()
                count += 1

            modeladmin.message_user(request, 'Бренд от поставщика {} '
                                             'применен к {} товарам.'.
                                    format(brand, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeProductBrandForm(initial={'_selected_action': request.
                                    POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/product_add_brand.html', {'items': queryset,
                                                                      'form': form,
                                                                      'title': 'Добавить бренд '
                                                                               'от поставщика'})


product_add_brand.short_description = 'Добавить БРЕНД ОТ ПОСТАВЩИКА'


def product_clear_brand(modeladmin, request, queryset):
    for item in queryset:
        item.brand.clear()


product_clear_brand.short_description = 'Очистить поле БРЕНД ОТ ПОСТАВЩИКА'


def product_add_status(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeProductStatusForm(request.POST)

        if form.is_valid():
            status = form.cleaned_data['status']

            count = 0
            for item in queryset:
                item.status = status
                item.save()
                count += 1

            modeladmin.message_user(request, 'Статус {} '
                                             'применен к {} товарам.'.
                                    format(status, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeProductStatusForm(initial={'_selected_action': request.
                                     POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/product_add_status.html', {'items': queryset,
                                                                       'form': form,
                                                                       'title': 'Добавить статус'})


product_add_status.short_description = 'Добавить СТАТУС'


def product_clear_status(modeladmin, request, queryset):
    for item in queryset:
        item.status.clear()


product_clear_status.short_description = 'Очистить поле СТАТУС'


def product_add_maker(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeProductMakerForm(request.POST)

        if form.is_valid():
            maker = form.cleaned_data['maker']

            count = 0
            for item in queryset:
                item.maker = maker
                item.save()
                count += 1

            modeladmin.message_user(request, 'Поставщик {} '
                                             'применен к {} товарам.'.
                                    format(maker, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeProductMakerForm(initial={'_selected_action': request.
                                    POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/product_add_maker.html', {'items': queryset,
                                                                      'form': form,
                                                                      'title': 'Добавить поставщика'})


product_add_maker.short_description = 'Добавить ПОСТАВЩИКА'


def product_clear_maker(modeladmin, request, queryset):
    for item in queryset:
        item.maker.clear()


product_clear_maker.short_description = 'Очистить поле ПОСТАВЩИКА'


def category_xml_add_category_site(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeCategoryXMLCategorySiteForm(request.POST)

        if form.is_valid():
            category_site = form.cleaned_data['category_site']

            count = 0
            for item in queryset:
                item.category_site = category_site
                item.save()
                count += 1

            modeladmin.message_user(request, 'Категория на сайте {} '
                                             'применена к {} категориям от поставщика.'.
                                    format(category_site, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeCategoryXMLCategorySiteForm(initial={'_selected_action': request.
                                             POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/category_xml_add_category_site.html', {'items': queryset,
                                                                                   'form': form,
                                                                                   'title': 'Добавление категории '
                                                                                            'на сайте'})

category_xml_add_category_site.short_description = 'Добавить КАТЕГОРИЮ НА САЙТЕ'


def category_xml_clear_category_site(modeladmin, request, queryset):
    for item in queryset:
        item.category_site.clear()

category_xml_clear_category_site.short_description = 'Очистить поле КАТЕГОРИЯ НА САЙТЕ'


def category_xml_add_maker(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeCategoryXMLMakerForm(request.POST)

        if form.is_valid():
            maker = form.cleaned_data['maker']

            count = 0
            for item in queryset:
                item.maker = maker
                item.save()
                count += 1

            modeladmin.message_user(request, 'Поставщик {} '
                                             'применен к {} категориям от поставщика.'.
                                    format(maker, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeCategoryXMLMakerForm(initial={'_selected_action': request.
                                          POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/category_xml_add_maker.html', {'items': queryset,
                                                                           'form': form,
                                                                           'title': 'Изменение поставщика'})


category_xml_add_maker.short_description = 'Изменить ПОСТАВЩИКА'


def brand_maker_add_brand(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeBrandMakerBrandForm(request.POST)

        if form.is_valid():
            brand = form.cleaned_data['brand']

            count = 0
            for item in queryset:
                item.brand = brand
                item.save()
                count += 1

            modeladmin.message_user(request, 'Бренд на сайте {} '
                                             'применен к {} брендам от поставщика.'.
                                    format(brand, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeBrandMakerBrandForm(initial={'_selected_action': request.
                                         POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/brand_maker_add_brand.html', {'items': queryset,
                                                                          'form': form,
                                                                          'title': 'Добавление бренда '
                                                                                   'на сайт'})


brand_maker_add_brand.short_description = 'Добавить БРЕНД НА САЙТЕ'


def brand_maker_clear_brand(modeladmin, request, queryset):
    for item in queryset:
        item.brand.clear()


brand_maker_clear_brand.short_description = 'Очистить поле БРЕНД НА САЙТЕ'


def print_type_maker_add_print_type(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangePrintTypeMakerPrintTypeForm(request.POST)

        if form.is_valid():
            print_type = form.cleaned_data['print_type']

            count = 0
            for item in queryset:
                item.print_type = print_type
                item.save()
                count += 1

            modeladmin.message_user(request, 'Вид нанесения от поставщика {} '
                                             'применен к {} видам нанесения на сайте.'.
                                    format(print_type, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangePrintTypeMakerPrintTypeForm(initial={'_selected_action': request.
                                         POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/print_type_maker_add_print_type.html', {'items': queryset,
                                                                                    'form': form,
                                                                                    'title': 'Добавление вида нанесения'
                                                                                             'на сайт'})

print_type_maker_add_print_type.short_description = 'Добавить ВИД НАНЕСЕНИЯ НА САЙТЕ'


def print_type_maker_clear_print_type(modeladmin, request, queryset):
    for item in queryset:
        item.print_type.clear()

print_type_maker_clear_print_type.short_description = 'Очистить поле ВИД НАНЕСЕНИЯ НА САЙТЕ'
