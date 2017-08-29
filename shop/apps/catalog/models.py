# -*- coding: utf-8 -*-

import os

from smart_selects.db_fields import ChainedForeignKey
from treebeard.mp_tree import MP_Node
from pytils.translit import slugify
import hashlib

from django.contrib.contenttypes.models import ContentType
from django.db import models


class Maker(models.Model):

    name = models.CharField(verbose_name='Поставщик', max_length=255, unique=True)
    official = models.CharField(verbose_name='Наименование поставщика', max_length=255)

    def save(self, **kwargs):
        if not self.id:
            self.name = slugify(self.official)
        super(Maker, self).save(**kwargs)

    class Meta:

        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.official


class Brand(models.Model):
    name = models.CharField(verbose_name='Бренд', max_length=255, unique=True)
    official = models.CharField(verbose_name='Наименование бренда', max_length=255)

    def save(self, **kwargs):
        if not self.id:
            self.name = slugify(self.official)
        super(Brand, self).save(**kwargs)

    class Meta:
        verbose_name = 'Бренд на сайте'
        verbose_name_plural = 'Бренд на сайте'

    def __str__(self):
        return self.official


class BrandMaker(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    title = models.CharField(verbose_name='Наименование', max_length=255, blank=True)
    code = models.CharField(verbose_name='Код', max_length=255, blank=True)
    brand = models.ForeignKey(Brand, verbose_name='Бренд на сайте', null=True, blank=True)
    prov_brand_id = models.CharField(verbose_name='ИД', max_length=255, blank=True)

    class Meta:
        unique_together = ('maker', 'title')
        verbose_name = 'Брэнд от поставщика'
        verbose_name_plural = 'Брэнды от поставщика'

    def __str__(self):
        return u'{} ({})'.format(self.title, self.maker)


class CategorySite(MP_Node):

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', unique=True, blank=True)
    preview = models.TextField(verbose_name='Краткое описание', blank=True, null=True)
    content = models.TextField(verbose_name='Описание', blank=True, null=True)
    show = models.BooleanField(verbose_name='Показывать', default=True)
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True)
    position = models.IntegerField(verbose_name='Позиция', blank=True, null=True)

    def get_children(self):
        return CategorySite.get_children(self).filter(show=True)

    def save(self, **kwargs):
        if not self.id:
            self.slug_title = slugify(self.title)
        super(CategorySite, self).save(**kwargs)

    class Meta:
        verbose_name = 'Категория на сайте'
        verbose_name_plural = 'Категории на сайте'

    def __str__(self):
        return '{}{}'.format((self.depth - 1) * '---', self.slug_title)


class CategoryXML(MP_Node):

    def default_cat_id(self):
        return hashlib.md5(slugify(self.title).encode(encoding='utf-8')).hexdigest()

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    title = models.CharField(verbose_name='Заголовок', max_length=255, blank=False)
    cat_id = models.CharField(verbose_name='ИД', max_length=100)
    category_site = models.ForeignKey(CategorySite, verbose_name='Категория на сайте',
                                      blank=True, null=True, related_name='category_xml_s')
    status = models.ForeignKey('Status', verbose_name='Статус', blank=True, null=True)
    import_fl = models.BooleanField(verbose_name='Импортирован в базу', default=False)

    class Meta:
        unique_together = ('maker', 'cat_id')
        verbose_name = 'Категория от поставщика'
        verbose_name_plural = 'Категории от поставщиков'

    def save(self, **kwargs):
        if not self.id and not self.import_fl:
            self.cat_id = self.default_cat_id()
        super(CategoryXML, self).save()

    def __str__(self):
        return u'{}{} ({})'.format((self.depth - 1) * u'---', self.title, self.maker)


class Status(models.Model):

    name = models.CharField(verbose_name='Статус', max_length=255, unique=True)
    official = models.CharField(verbose_name='Наименование статуса', max_length=255)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def save(self, **kwargs):
        if not self.id:
            self.name = slugify(self.official)
        super(Status, self).save(**kwargs)

    def __str__(self):
        return self.official


class PrintType(models.Model):
    name = models.CharField(verbose_name='Вид нанесения', max_length=255, unique=True)
    official = models.CharField(verbose_name='Наименование вида нанесения', max_length=255)

    def save(self, **kwargs):
        if not self.id:
            self.name = slugify(self.official)
        super(PrintType, self).save(**kwargs)

    class Meta:
        verbose_name = 'Вид нанесения на сайте'
        verbose_name_plural = 'Виды нанесения на сайте'

    def __str__(self):
        return self.official


class PrintTypeMaker(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    code = models.CharField(verbose_name='Код', max_length=100)
    title = models.CharField(verbose_name='Название', max_length=255)
    desc = models.CharField(verbose_name='Описание', max_length=1000)
    print_type = models.ForeignKey(PrintType, verbose_name='Вид нанесения на сайте',
                                   null=True, blank=True)

    class Meta:
        unique_together = ('maker', 'title')
        verbose_name = 'Вид нанесения от поставщика'
        verbose_name_plural = 'Виды нанесения от поставщика'

    def __str__(self):
        return u'{} ({})'.format(self.title, self.maker)


class ProductType(models.Model):

    name = models.CharField(verbose_name='Тип продукта', max_length=255, unique=True)
    official = models.CharField(verbose_name='Наименование тип продукта', max_length=255)

    def save(self, **kwargs):
        if not self.id:
            self.name = slugify(self.official)
        super(ProductType, self).save(**kwargs)

    class Meta:

        verbose_name = 'Тип продукта'
        verbose_name_plural = 'Тип продукта'

    def __str__(self):
        return self.official


class Product(models.Model):

    def default_slug_title(self):
        return slugify('{}_{}_{}'.format(self.maker, self.title, self.code))[:255]

    def default_code(self):
        return hashlib.md5(slugify(self.title).encode(encoding='utf-8')).hexdigest()

    def product_upload_path(self, instance):
        return os.path.join('upload_product', self.maker.name, '{}{}'.
                            format(hashlib.md5(slugify(self.title).
                                               encode(encoding='utf-8')).hexdigest(), '.jpg'))

    parent = models.ForeignKey("self", verbose_name='Основной продукт', on_delete=models.CASCADE)
    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    title = models.CharField(verbose_name='Заголовок', max_length=255, blank=False)
    prov_product_id = models.CharField(verbose_name='ИД', max_length=50, blank=True)
    prov_main_product_id = models.CharField(verbose_name='ИД родителя', max_length=50)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', max_length=255,
                                  blank=True, unique=True)
    code = models.CharField(verbose_name='Артикул', max_length=50, blank=True)
    content = models.TextField(verbose_name='Описание', blank=True)
    long_content = models.TextField(verbose_name='Полное описание', blank=True)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=10,
                                null=True)
    stock = models.IntegerField(verbose_name='Остаток', null=True, blank=True, default=None)

    brand = ChainedForeignKey(BrandMaker,
                              chained_field='maker',
                              chained_model_field='maker',
                              show_all=False,
                              auto_choose=False,
                              verbose_name='Бренд от поставщика',
                              blank=True,
                              null=True)

    status = models.ForeignKey(Status, verbose_name='Статус', blank=True, null=True)
    category_xml = models.ManyToManyField(CategoryXML,
                                          verbose_name=u'Категория для товара',
                                          blank=True)
    print_type = models.ManyToManyField(PrintTypeMaker,
                                        verbose_name=u'Вид нанесения от поставщика',
                                        blank=True)
    show = models.BooleanField(verbose_name='Показывать', default=True)
    import_fl = models.BooleanField(verbose_name='Импортирован в базу', default=False)

    def photos(self):
        return ProductAttachment.objects.filter(product=self, meaning=1).all()

    def main_image(self):
        return ProductAttachment.objects.filter(product=self, meaning=1, position=0).first()

    @staticmethod
    def get_model_id():
        return ContentType.objects.get(app_label='catalog', model='product').id

    def get_model_name(self):
        return ContentType.objects.get_for_model(self)

    def save(self, **kwargs):
        if not self.id and not self.import_fl:
            self.code = self.code or self.default_code()
            self.slug_title = self.default_slug_title()
        super(Product, self).save()

    class Meta:
        unique_together = ('maker', 'code')
        ordering = ('price',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class ProductPackKV(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    product = models.ForeignKey(Product, verbose_name='Товар')
    pack_id = models.IntegerField(verbose_name='Порядковый номер пакета у товара',
                                  default=0)
    abbr = models.CharField(verbose_name='Название поля (поиск)', max_length=255)
    name = models.CharField(verbose_name='Имя поля', max_length=255)
    value = models.CharField(verbose_name='Значение поля', max_length=255)
    position = models.IntegerField(verbose_name='Порядок', null=True)

    class Meta:
        unique_together = ('product', 'pack_id', 'abbr')


class ProductStock(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    product = models.ForeignKey(Product, verbose_name='Товар')

    geo = models.CharField(verbose_name='ГеоМетка', max_length=100)
    type = models.CharField(verbose_name='Тип', max_length=255)
    value = models.IntegerField(verbose_name='Значение поля')

    class Meta:
        unique_together = ('product', 'abbr')


class ProductParamsKV(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    product = models.ForeignKey(Product, verbose_name='Товар')

    abbr = models.CharField(verbose_name='Название поля (поиск)', max_length=255)
    name = models.CharField(verbose_name='Имя поля', max_length=255)
    value = models.CharField(verbose_name='Значение поля', max_length=4000)
    position = models.IntegerField(verbose_name='Порядок', null=True)

    class Meta:
        unique_together = ('product', 'abbr')


class ProductAttachment(models.Model):

    MEANINGS = (
        (0, 'Изображение'),
        (1, 'Файл')
    )

    def product_attachment_upload_path(self):
        return os.path.join('upload_attachment', self.maker.name, '{}{}'.
                            format(hashlib.md5(slugify(self.desc).
                                               encode(encoding='utf-8')).hexdigest(), '.jpg'))

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    product = models.ForeignKey(Product, verbose_name='Товар')
    meaning = models.IntegerField(verbose_name='Тип файла', choices=MEANINGS)
    file = models.FileField(verbose_name='URL файла',
                            upload_to=product_attachment_upload_path,
                            blank=True)
    image = models.ImageField(verbose_name='URL картинки',
                              upload_to=product_attachment_upload_path,
                              blank=True)
    type = models.CharField(verbose_name='Тип', max_length=20)
    desc = models.CharField(verbose_name='Описание', max_length=255)
    position = models.IntegerField(verbose_name='Порядок', null=True)

    def save(self, **kwargs):
        self.maker = self.product.maker
        super(ProductAttachment, self).save()

    class Meta:
        verbose_name = 'Файл (изображение)'
        verbose_name_plural = 'Файлы (изображения)'

    def __str__(self):
        return self.desc


class Settings(models.Model):

    title = models.CharField(verbose_name='Заголовок раздела', max_length=128)
    content = models.TextField(verbose_name='Контент основной страницы раздела',
                               blank=True, null=True)

    class Meta:
        verbose_name = 'Настройка раздела Каталог'
        verbose_name_plural = 'Настройки раздела Каталог'
