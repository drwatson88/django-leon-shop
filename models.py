# -*- coding: utf-8 -*-

import os

from django.db import models
from treebeard.mp_tree import MP_Node
from django.contrib.contenttypes.models import ContentType
from pytils.translit import slugify


class Maker(models.Model):
    name = models.CharField(verbose_name='Поставщик', max_length=255, unique=True)
    official = models.CharField(verbose_name='Наименование поставщика', max_length=255)

    class Meta:

        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __unicode__(self):
        return self.name


class Brand(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    name = models.CharField(verbose_name='Наименование', max_length=255, blank=True)
    code = models.CharField(verbose_name='Код', max_length=255, blank=True)
    brand_id = models.CharField(verbose_name='ИД', max_length=255)

    class Meta:
        unique_together = ('maker', 'name')
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'

    def __unicode__(self):
        return self.name


class Category(MP_Node):

    name = models.CharField(verbose_name='Заголовок', max_length=255)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', unique=True)
    preview = models.TextField(verbose_name='Краткое описание')
    content = models.TextField(verbose_name='Описание', blank=True, null=True)
    show = models.BooleanField(verbose_name='Показывать', default=True)
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True)
    position = models.IntegerField(verbose_name='Позиция', blank=True, null=True)

    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True, null=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255, blank=True, null=True)
    metakey = models.CharField(verbose_name='Meta key', max_length=255, blank=True, null=True)
    metades = models.CharField(verbose_name='Meta des', max_length=255, blank=True, null=True)

    def getchildrens(self):
        return Category.get_children(self).filter(show=True)

    def save(self, **kwargs):
        if not self.id:
            self.slug_title = slugify(self.slug_title)
        super(Category, self).save(**kwargs)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __unicode__(self):
        return u'{}{}'.format((self.depth - 1) * u'---', self.name)


class CategoryXML(MP_Node):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    name = models.CharField(verbose_name='Заголовок', max_length=255)
    cat_id = models.CharField(verbose_name='ИД', max_length=100)
    category = models.ForeignKey(Category, verbose_name='Категория на сайте',
                                 blank=True, null=True, related_name='categorys_xml')
    status = models.ForeignKey('Status', verbose_name='Статус', blank=True, null=True)

    class Meta:
        unique_together = ('maker', 'cat_id')
        verbose_name = 'Категорию от поставщика'
        verbose_name_plural = 'Категории от поставщиков'

    def __unicode__(self):
        return u'{}{} ({})'.format((self.depth - 1) * u'---', self.name, self.maker)


class Status(models.Model):

    name = models.CharField(verbose_name='Статус', max_length=255, unique=True)
    official = models.CharField(verbose_name='Наименование статуса', max_length=255)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __unicode__(self):
        return self.name


class PrintType(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    code = models.CharField(verbose_name='Код', max_length=100)
    name = models.CharField(verbose_name='Название', max_length=255)
    desc = models.CharField(verbose_name='Описание', max_length=1000)

    class Meta:
        unique_together = ('maker', 'name')
        verbose_name = 'Вид нанесения'
        verbose_name_plural = 'Виды нанесения'

    def __unicode__(self):
        return self.name


class Tovar(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    name = models.CharField(verbose_name='Заголовок', max_length=255)
    product_id = models.CharField(verbose_name='ИД', max_length=50)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', max_length=255,
                                  unique=True)

    code = models.CharField(verbose_name='Артикул', max_length=50)
    content = models.TextField(verbose_name='Описание')
    long_content = models.TextField(verbose_name='Полное описание')
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=10, null=True)
    stock = models.IntegerField(verbose_name='Остаток', null=True, blank=True, default=None)

    small_image = models.ImageField(verbose_name='Путь к файлу картинки 200х200',
                                    blank=True, null=True, max_length=255)
    big_image = models.ImageField(verbose_name='Путь к файлу картинки 280х280',
                                  blank=True, null=True, max_length=255)
    super_big_image = models.ImageField(verbose_name='Путь к файлу картинки 1000х1000',
                                        blank=True, null=True, max_length=255)

    brand = models.ForeignKey(Brand, verbose_name='Брэнд', blank=True, null=True)
    status = models.ForeignKey(Status, verbose_name='Статус', blank=True, null=True)
    categoryxml = models.ManyToManyField(CategoryXML, verbose_name='Категория для товара',
                                         blank=True, null=True)
    print_type = models.ManyToManyField(PrintType, verbose_name='Нанесение для товара',
                                        blank=True, null=True)
    show = models.BooleanField(verbose_name='Показывать', default=True)

    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True, null=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255, blank=True, null=True)
    metakey = models.CharField(verbose_name='Meta key', max_length=255, blank=True, null=True)
    metades = models.CharField(verbose_name='Meta des', max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def photos(self):
        return TovarAttachment.objects.filter(tovar=self, meaning=1)

    def get_type(self):
        return 1

    def save(self, **kwargs):
        if not self.id:
            self.slug_title = slugify(self.slug_title)
        super(Tovar, self).save()

    class Meta:
        unique_together = ('maker', 'code')
        ordering = ('price',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class TovarParamsPack(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    tovar = models.ForeignKey(Tovar, verbose_name='Товар')
    pack_id = models.IntegerField(verbose_name='Порядковый номер пакета у товара', default=0)
    abbr = models.CharField(verbose_name='Название поля (поиск)', max_length=255)
    name = models.CharField(verbose_name='Имя поля', max_length=255)
    value = models.CharField(verbose_name='Значение поля', max_length=255)
    position = models.IntegerField(verbose_name='Порядок', null=True)

    class Meta:
        unique_together = ('tovar', 'pack_id', 'abbr')


class TovarParamsStock(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    tovar = models.ForeignKey(Tovar, verbose_name='Товар')
    abbr = models.CharField(verbose_name='Название поля (поиск)', max_length=255)
    name = models.CharField(verbose_name='Имя поля', max_length=255)
    value = models.CharField(verbose_name='Значение поля', max_length=255)
    position = models.IntegerField(verbose_name='Порядок', null=True)

    class Meta:
        unique_together = ('tovar', 'abbr')


class TovarParamsOther(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    tovar = models.ForeignKey(Tovar, verbose_name='Товар')
    abbr = models.CharField(verbose_name='Название поля (поиск)', max_length=255)
    name = models.CharField(verbose_name='Имя поля', max_length=255)
    value = models.CharField(verbose_name='Значение поля', max_length=4000)
    position = models.IntegerField(verbose_name='Порядок', null=True)

    class Meta:
        unique_together = ('tovar', 'abbr')


class SubTovar(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    tovar = models.ForeignKey(Tovar, verbose_name='Товар')

    name = models.CharField(verbose_name='Заголовок', max_length=255)
    code = models.CharField(verbose_name='Артикул', max_length=50)
    product_id = models.CharField(verbose_name='ИД', max_length=50)
    main_product_id = models.CharField(verbose_name='ИД родителя', max_length=50)

    price = models.DecimalField(verbose_name='Цена', decimal_places=2,
                                max_digits=10, null=True)

    class Meta:
        unique_together = ('maker', 'code')

    def get_type(self):
        return 0


class SubTovarParamsStock(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    subtovar = models.ForeignKey(SubTovar, verbose_name='Субтовар')
    abbr = models.CharField(verbose_name='Название поля (поиск)', max_length=255)
    name = models.CharField(verbose_name='Имя поля', max_length=255)
    value = models.CharField(verbose_name='Значение поля', max_length=255)
    position = models.IntegerField(verbose_name='Порядок', null=True)

    class Meta:
        unique_together = ('subtovar', 'abbr')


class SubTovarParamsOther(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    subtovar = models.ForeignKey(SubTovar, verbose_name='Субтовар')
    abbr = models.CharField(verbose_name='Название поля (поиск)', max_length=255)
    name = models.CharField(verbose_name='Имя поля', max_length=255)
    value = models.CharField(verbose_name='Значение поля', max_length=255)
    position = models.IntegerField(verbose_name='Порядок', null=True)

    class Meta:
        unique_together = ('subtovar', 'abbr')


class TovarAttachment(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    tovar = models.ForeignKey(Tovar, verbose_name='Товар')
    meaning = models.IntegerField(verbose_name='Тип файла')
    file = models.FileField(verbose_name='URL доп.файла', blank=True, null=True)
    image = models.ImageField(verbose_name='URL доп.картинки', blank=True, null=True)
    name = models.CharField(verbose_name='Описание доп.файла или картинки', max_length=255)

    class Meta:
        unique_together = ('tovar', 'image', 'file')


class MSettings(models.Model):

    title = models.CharField(verbose_name='Заголовок раздела', max_length=128)
    content = models.TextField(verbose_name='Контент основной страницы раздела', blank=True, null=True)

    class Meta:
        verbose_name = 'Настройка раздела Каталог'
        verbose_name_plural = 'Настройки раздела Каталог'