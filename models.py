# -*- coding: utf-8 -*-

import os

from django.db import models
from treebeard.mp_tree import MP_Node
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from pytils.translit import slugify


def path_for_cat_image(instance, filename):
    file_path, file_ext = os.path.splitext(unicode(filename))
    return '{}/{}/{}{}'.format('upload_category', os.path.split(file_path)[0],
                                slugify(os.path.split(file_path)[1]), file_ext)

def path_for_tovar_image(instance, filename):
    _filename, _fileext = os.path.splitext(unicode(filename))
    return 'upload_tovar/' + slugify(_filename) + _fileext

def path_for_tovar_attach(instance, filename):
    _filename, _fileext = os.path.splitext(unicode(filename))
    return 'upload_tovar/' + slugify(_filename) + _fileext


class Maker(models.Model):

    name = models.CharField('Поставщик', max_length=255)
    code = models.IntegerField("Код")

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __unicode__(self):
        return self.name


class Category(MP_Node):

    parent = models.ForeignKey('self', verbose_name='Категория', blank=True, null=True, editable=False)
    name = models.CharField('Заголовок', max_length=255)
    slug_title = models.SlugField('Имя для ссылки', unique=False)
    preview = models.CharField('Краткое описание', max_length=2550)
    content = models.TextField('Описание', blank=True, null=True)
    contentSEO = models.TextField('Описание для SEO', blank=True, null=True)
    show = models.BooleanField('Показывать', default=True)
    image = models.ImageField('Изображение', upload_to=path_for_cat_image, blank=True, null=True)
    uri = models.CharField('Имя ссылки', max_length=255)
    position = models.IntegerField('Позиция', blank=True, null=True)

    title_seo = models.CharField('Заголовок для SEO', max_length=255, blank=True, null=True)
    metakey = models.CharField('Meta key', max_length=255, blank=True, null=True)
    metades = models.CharField('Meta des', max_length=255, blank=True, null=True)

    def getchildrens(self):
        return Category.get_children(self).filter(show=True)

    def save(self):
        if not self.id:
            self.slug_title = slugify(self.slug_title)
        super(Category, self).save()

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __unicode__(self):
        return (self.depth - 1) * "---" + self.name


class CategoryXML(MP_Node):

    parent = models.ForeignKey('self', verbose_name='Категория', blank=True, null=True, editable=False)
    name = models.CharField('Заголовок', max_length=255)
    page_id = models.CharField('id категории в системе поставщика', blank=True, null=True, max_length=100)
    uri = models.CharField('Имя ссылки', max_length=255)
    category = models.ForeignKey(Category, verbose_name='Категория на сайте', blank=True, null=True,
                                 related_name='categorys_xml')
    maker = models.ForeignKey(Maker)

    class Meta:
        verbose_name = 'Категорию от поставщика'
        verbose_name_plural = 'Категории от поставщиков'

    def __unicode__(self):
        return (self.depth - 1) * "---" + self.name


class Group(models.Model):

    group_id = models.IntegerField('id группы в системе поставщика', blank=True, null=True)


class Status(models.Model):

    name = models.CharField('Статус', max_length=255)
    status_id = models.IntegerField('id статуса в системе поставщика', blank=True, null=True)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __unicode__(self):
        return self.name


class PrintType(models.Model):

    name = models.CharField('Код вида нанесения', max_length=100)
    description = models.CharField('Название вида нанесения', max_length=255)

    class Meta:
        verbose_name = 'Вид нанесения'
        verbose_name_plural = 'Виды нанесения'

    def __unicode__(self):
        return self.description


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
    amount = models.IntegerField('Всего на складе')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    # free = models.IntegerField(u'Доступно для резервирования')
    # inwayamount = models.IntegerField(u'Всего в пути (поставка)')
    # inwayfree = models.IntegerField(u'Доступно для резервирования из поставки')
    # enduserprice = models.IntegerField(u'Цена End-User')


class Tovar(models.Model):

    name = models.CharField('Заголовок', max_length=255)
    product_id = models.CharField('id товара в системе поставщика', max_length=50)
    categoryxml = models.ManyToManyField(CategoryXML, verbose_name='Категория для товара', blank=True, null=True)
    slug_title = models.SlugField('Имя для ссылки', unique=False)
    group = models.ForeignKey(Group, verbose_name='Группа товара', blank=True, null=True)
    status = models.ForeignKey(Status, verbose_name='Статус', blank=True, null=True)
    code = models.CharField('Артикул', max_length=50)
    product_size = models.CharField('Размеры', max_length=200)
    matherial = models.CharField('Материал', max_length=50)
    small_image = models.ImageField('Путь к файлу картинки 200х200', upload_to=path_for_tovar_image, blank=True, null=True)
    big_image = models.ImageField('Путь к файлу картинки 280х280', upload_to=path_for_tovar_image, blank=True, null=True)
    super_big_image = models.ImageField('Путь к файлу картинки 1000х1000', upload_to=path_for_tovar_image, blank=True, null=True)
    content = models.CharField('Описание', max_length=4000)
    brand = models.CharField('Бренд', max_length=50)
    weight = models.DecimalField('Вес',  decimal_places=2, max_digits=10)
    price = models.DecimalField('Цена',  decimal_places=2, max_digits=10)
    # filter = models.ManyToManyField(Filter, verbose_name=u'Фильтр для товара', blank=True, null=True)
    print_type = models.ManyToManyField(PrintType, verbose_name='Нанесение для товара', blank=True, null=True)
    maker = models.ForeignKey(Maker)
    stock = generic.GenericRelation(Stock)

    def __unicode__(self):
        return self.name

    def photos(self):
        return TovarAttachment.objects.filter(tovar=self, meaning=1)

    def get_type(self):
        return 1

    def save(self):
        if not self.id:
            self.slug_title = slugify(self.slug_title)
        super(Tovar, self).save()

    class Meta:
        ordering = ('price',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class SubTovar(models.Model):

    name = models.CharField('Заголовок', max_length=255)
    code = models.CharField('Артикул', max_length=50)
    product_id = models.CharField('id товара в системе поставщика', max_length=50)
    main_product_id = models.CharField('id основного товара в системе поставщика', max_length=50)
    size_code = models.CharField('Размер', max_length=50)
    weight = models.DecimalField('Вес', decimal_places=2, max_digits=10)
    price = models.DecimalField('Цена', decimal_places=2, max_digits=10)
    tovar = models.ForeignKey(Tovar)
    maker = models.ForeignKey(Maker)
    stock = generic.GenericRelation(Stock)

    def get_type(self):
        return 0


class Pack(models.Model):

    amount = models.IntegerField('Количество в упаковке')
    weight = models.DecimalField('Вес упаковки', decimal_places=2, max_digits=10)
    volume = models.DecimalField('Объем упаковки', decimal_places=2, max_digits=10)
    sizex = models.DecimalField('Размер длина', decimal_places=1, max_digits=10)
    sizey = models.DecimalField('Размер ширина', decimal_places=1, max_digits=10)
    sizez = models.DecimalField('Размер высота', decimal_places=1, max_digits=10)
    tovar = models.ForeignKey(Tovar)


class TovarAttachment(models.Model):

    meaning = models.IntegerField('Тип файла')
    file = models.FileField('URL доп.файла', upload_to=path_for_tovar_attach, blank=True, null=True)
    image = models.ImageField('URL доп.картинки', upload_to=path_for_tovar_attach, blank=True, null=True)
    name = models.CharField('Описание доп.файла или картинки', max_length=255)
    tovar = models.ForeignKey(Tovar)


class MSettings(models.Model):

    title = models.CharField('Заголовок раздела', max_length=128)
    content = models.TextField('Контент основной страницы раздела', blank=True, null=True)
    contentSEO = models.TextField('Контент для SEO', blank=True, null=True)
    metatitle = models.CharField('Заголовок для SEO', max_length=1000, blank=True, null=True)
    metakey = models.CharField('Meta key', max_length=5000, blank=True, null=True)
    metades = models.CharField('Meta des', max_length=5000, blank=True, null=True)

    class Meta:
        verbose_name = 'Настройка раздела Каталог'
        verbose_name_plural = 'Настройки раздела Каталог'