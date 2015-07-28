# -*- coding: utf-8 -*-

import os

from django.db import models
from treebeard.mp_tree import MP_Node
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from pytils.translit import slugify


class Maker(models.Model):

    name = models.CharField(u'Поставщик', max_length=255)
    code = models.IntegerField(u"Код")


class Category(MP_Node):

    def path_for_object(instance, filename):
        file_path, file_ext = os.path.splitext(unicode(filename))
        return u'{}/{}/{}{}'.format(u'upload_category', os.path.split(file_path)[0],
                                  slugify(os.path.split(file_path)[1]), file_ext)

    parent = models.ForeignKey(u'self', verbose_name=u'Категория', blank=True, null=True, editable=False)
    name = models.CharField(u'Заголовок', max_length=255)
    show = models.BooleanField(u'Показывать', default=True)
    image = models.ImageField(u'Изображение', upload_to=path_for_object, blank=True, null=True)
    uri = models.CharField(u'Имя ссылки', max_length=255)

    def getchildrens(self):
        return Category.get_children(self).filter(show=True)


class CategoryXML(MP_Node):

    parent = models.ForeignKey(u'self', verbose_name=u'Категория', blank=True, null=True, editable=False)
    name = models.CharField(u'Заголовок', max_length=255)
    page_id = models.CharField(u'id категории в системе поставщика', blank=True, null=True, max_length=100)
    uri = models.CharField(u'Имя ссылки', max_length=255)
    category = models.ForeignKey(Category, verbose_name=u'Категория на сайте', blank=True, null=True, related_name=u'categorys_xml')
    maker = models.ForeignKey(Maker)


class Group(models.Model):

    group_id = models.IntegerField(u'id группы в системе поставщика', blank=True, null=True)


class Status(models.Model):

    name = models.CharField(u'Статус', max_length=255)
    status_id = models.IntegerField(u'id статуса в системе поставщика', blank=True, null=True)


class PrintType(models.Model):

    name = models.CharField(u'Код вида нанесения', max_length=100)
    description = models.CharField(u'Название вида нанесения', max_length=255)


# class FilterType(models.Model):
#
#     filter_type_id = models.CharField(u'id типа фильтра в системе поставщика', max_length=50)
#     filter_type_name = models.CharField(u'Название типа фильтра', max_length=255)
#
#
# class Filter(models.Model):
#
#     filter_id = models.CharField(u'id фильтра в системе поставщика', max_length=50)
#     filter_name = models.CharField(u'Название фильтра', max_length=50)
#     filter_type = models.ForeignKey(FilterType)


class Stock(models.Model):

    # product_id = models.CharField(u'id товара в системе поставщика', max_length=50)
    # code = models.CharField(u'Артикул', max_length=50)
    amount = models.IntegerField(u'Всего на складе')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey(u'content_type', u'object_id')

    # free = models.IntegerField(u'Доступно для резервирования')
    # inwayamount = models.IntegerField(u'Всего в пути (поставка)')
    # inwayfree = models.IntegerField(u'Доступно для резервирования из поставки')
    # enduserprice = models.IntegerField(u'Цена End-User')


class Tovar(models.Model):

    def path_for_object(instance, filename):
        _filename, _fileext = os.path.splitext(unicode(filename))
        return u'upload_tovar/' + slugify(_filename) + _fileext

    name = models.CharField(u'Заголовок', max_length=255)
    product_id = models.CharField(u'id товара в системе поставщика', max_length=50)
    categoryxml = models.ManyToManyField(CategoryXML, verbose_name=u'Категория для товара', blank=True, null=True)
    group = models.ForeignKey(Group, verbose_name=u'Группа товара', blank=True, null=True)
    status = models.ForeignKey(Status, verbose_name=u'Статус', blank=True, null=True)
    code = models.CharField(u'Артикул', max_length=50)
    product_size = models.CharField(u'Размеры', max_length=50)
    matherial = models.CharField(u'Материал', max_length=50)
    small_image = models.ImageField(u'Путь к файлу картинки 200х200', upload_to=path_for_object, blank=True, null=True)
    big_image = models.ImageField(u'Путь к файлу картинки 280х280', upload_to=path_for_object, blank=True, null=True)
    super_big_image = models.ImageField(u'Путь к файлу картинки 1000х1000', upload_to=path_for_object, blank=True, null=True)
    content = models.CharField(u'Описание', max_length=1000)
    brand = models.CharField(u'Бренд', max_length=50)
    weight = models.DecimalField(u'Вес',  decimal_places=2, max_digits=10)
    price = models.DecimalField(u'Цена',  decimal_places=2, max_digits=10)
    # filter = models.ManyToManyField(Filter, verbose_name=u'Фильтр для товара', blank=True, null=True)
    print_type = models.ManyToManyField(PrintType, verbose_name=u'Нанесение для товара', blank=True, null=True)
    maker = models.ForeignKey(Maker)
    stock = generic.GenericRelation(Stock)


class SubTovar(models.Model):

    name = models.CharField(u'Заголовок', max_length=255)
    code = models.CharField(u'Артикул', max_length=50)
    product_id = models.CharField(u'id товара в системе поставщика', max_length=50)
    main_product_id = models.CharField(u'id основного товара в системе поставщика', max_length=50)
    size_code = models.CharField(u'Размер', max_length=50)
    weight = models.DecimalField(u'Вес', decimal_places=2, max_digits=10)
    price = models.DecimalField(u'Цена', decimal_places=2, max_digits=10)
    tovar = models.ForeignKey(Tovar)
    maker = models.ForeignKey(Maker)
    stock = generic.GenericRelation(Stock)


class Pack(models.Model):

    amount = models.IntegerField(u'Количество в упаковке')
    weight = models.DecimalField(u'Вес упаковки', decimal_places=2, max_digits=10)
    volume = models.DecimalField(u'Объем упаковки', decimal_places=2, max_digits=10)
    sizex = models.DecimalField(u'Размер длина', decimal_places=1, max_digits=10)
    sizey = models.DecimalField(u'Размер ширина', decimal_places=1, max_digits=10)
    sizez = models.DecimalField(u'Размер высота', decimal_places=1, max_digits=10)
    tovar = models.ForeignKey(Tovar)


class TovarAttachment(models.Model):

    def path_for_object(instance, filename):
        _filename, _fileext = os.path.splitext(unicode(filename))
        return u'upload_tovar/' + slugify(_filename) + _fileext

    meaning = models.IntegerField(u'Тип файла')
    file = models.FileField(u'URL доп.файла', upload_to=path_for_object, blank=True, null=True)
    image = models.ImageField(u'URL доп.картинки', upload_to=path_for_object, blank=True, null=True)
    name = models.CharField(u'Описание доп.файла или картинки', max_length=255)
    tovar = models.ForeignKey(Tovar)