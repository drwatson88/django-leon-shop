# coding: utf-8


from admin_forms import ChangeTovarCategoryXMLForm, ChangeTovarPrintTypeForm, \
    ChangeCategoryXMLCategoryForm, ChangeBrandMakerBrandForm, \
    ChangePrintTypeMakerPrintTypeForm, ChangeCategoryXMLMakerForm, \
    ChangeTovarBrandForm, ChangeTovarMakerForm, ChangeTovarStatusForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import admin


def tovar_add_categoryxml(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeTovarCategoryXMLForm(request.POST)

        if form.is_valid():
            categoryxml = form.cleaned_data['categoryxml']

            count = 0
            for item in queryset:
                item.categoryxml.add(categoryxml)
                item.save()
                count += 1

            modeladmin.message_user(request, 'Категория от поставщика {} '
                                             'применена к {} товарам.'.
                                    format(categoryxml, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeTovarCategoryXMLForm(initial={'_selected_action': request.
                                          POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/tovar_add_categoryxml.html', {'items': queryset,
                                                                          'form': form,
                                                                          'title': 'Добавление категории '
                                                                                   'от поставщика'})

tovar_add_categoryxml.short_description = 'Добавить КАТЕГОРИЮ ОТ ПОСТАВЩИКА'


def tovar_clear_categoryxmls(modeladmin, request, queryset):
    for item in queryset:
        item.categoryxml.clear()

tovar_clear_categoryxmls.short_description = 'Очистить поле КАТЕГОРИИ ОТ ПОСТАВЩИКА'


def tovar_add_print_type(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeTovarPrintTypeForm(request.POST)

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
        form = ChangeTovarPrintTypeForm(initial={'_selected_action': request.
                                        POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/tovar_add_print_type.html', {'items': queryset,
                                                                         'form': form,
                                                                         'title': 'Добавить вид нанесения '
                                                                                  'от поставщика'})

tovar_add_print_type.short_description = 'Добавить ВИД НАНЕСЕНИЯ ОТ ПОСТАВЩИКА'


def tovar_clear_print_types(modeladmin, request, queryset):
    for item in queryset:
        item.print_type.clear()

tovar_clear_print_types.short_description = 'Очистить поле ВИДЫ НАНЕСЕНИЯ ОТ ПОСТАВЩИКА'


def tovar_add_brand(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeTovarBrandForm(request.POST)

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
        form = ChangeTovarBrandForm(initial={'_selected_action': request.
                                    POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/tovar_add_brand.html', {'items': queryset,
                                                                    'form': form,
                                                                    'title': 'Добавить бренд '
                                                                             'от поставщика'})


tovar_add_brand.short_description = 'Добавить БРЕНД ОТ ПОСТАВЩИКА'


def tovar_clear_brand(modeladmin, request, queryset):
    for item in queryset:
        item.brand.clear()


tovar_clear_brand.short_description = 'Очистить поле БРЕНД ОТ ПОСТАВЩИКА'


def tovar_add_status(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeTovarStatusForm(request.POST)

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
        form = ChangeTovarStatusForm(initial={'_selected_action': request.
                                     POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/tovar_add_status.html', {'items': queryset,
                                                                     'form': form,
                                                                     'title': 'Добавить статус'})


tovar_add_status.short_description = 'Добавить СТАТУС'


def tovar_clear_status(modeladmin, request, queryset):
    for item in queryset:
        item.status.clear()


tovar_clear_status.short_description = 'Очистить поле СТАТУС'


def tovar_add_maker(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeTovarMakerForm(request.POST)

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
        form = ChangeTovarMakerForm(initial={'_selected_action': request.
                                    POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/tovar_add_maker.html', {'items': queryset,
                                                                    'form': form,
                                                                    'title': 'Добавить поставщика'})


tovar_add_maker.short_description = 'Добавить ПОСТАВЩИКА'


def tovar_clear_maker(modeladmin, request, queryset):
    for item in queryset:
        item.maker.clear()


tovar_clear_maker.short_description = 'Очистить поле ПОСТАВЩИКА'


def categoryxml_add_category(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeCategoryXMLCategoryForm(request.POST)

        if form.is_valid():
            category = form.cleaned_data['category']

            count = 0
            for item in queryset:
                item.category = category
                item.save()
                count += 1

            modeladmin.message_user(request, 'Категория на сайте {} '
                                             'применена к {} категориям от поставщика.'.
                                    format(category, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeCategoryXMLCategoryForm(initial={'_selected_action': request.
                                             POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'catalog/actions/categoryxml_add_category.html', {'items': queryset,
                                                                             'form': form,
                                                                             'title': 'Добавление категории '
                                                                                      'на сайте'})

categoryxml_add_category.short_description = 'Добавить КАТЕГОРИЮ НА САЙТЕ'


def categoryxml_clear_category(modeladmin, request, queryset):
    for item in queryset:
        item.category.clear()

categoryxml_clear_category.short_description = 'Очистить поле КАТЕГОРИЯ НА САЙТЕ'


def categoryxml_add_maker(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = ChangeCategoryXMLMakerForm(request.POST)

        if form.is_valid():
            maker = form.cleaned_data['maker']

            print maker

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

    return render(request, 'catalog/actions/categoryxml_add_maker.html', {'items': queryset,
                                                                          'form': form,
                                                                          'title': 'Изменение поставщика'})


categoryxml_add_maker.short_description = 'Изменить ПОСТАВЩИКА'


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
                                                                                    'title': 'Добавление вида нанесения '
                                                                                             'на сайт'})

print_type_maker_add_print_type.short_description = 'Добавить ВИД НАНЕСЕНИЯ НА САЙТЕ'


def print_type_maker_clear_print_type(modeladmin, request, queryset):
    for item in queryset:
        item.print_type.clear()

print_type_maker_clear_print_type.short_description = 'Очистить поле ВИД НАНЕСЕНИЯ НА САЙТЕ'
