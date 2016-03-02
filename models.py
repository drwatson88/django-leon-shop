# -*- coding: utf-8 -*-

import os

from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from treebeard.mp_tree import MP_Node
from pytils.translit import slugify
import hashlib


class Maker(models.Model):

    name = models.CharField(verbose_name='Поставщик', max_length=255, unique=True)
    official = models.CharField(verbose_name='Наименование поставщика', max_length=255)

    class Meta:

        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __unicode__(self):
        return self.official


class Brand(models.Model):
    name = models.CharField(verbose_name='Бренд', max_length=255, unique=True)
    official = models.CharField(verbose_name='Наименование бренда', max_length=255)

    def save(self, **kwargs):
        if not self.id:
            self.official = slugify(self.name)
        super(Brand, self).save(**kwargs)

    class Meta:
        verbose_name = 'Бренд на сайте'
        verbose_name_plural = 'Бренд на сайте'

    def __unicode__(self):
        return self.official


class BrandMaker(models.Model):

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    name = models.CharField(verbose_name='Наименование', max_length=255, blank=True)
    code = models.CharField(verbose_name='Код', max_length=255, blank=True)
    brand = models.ForeignKey(Brand, verbose_name='Бренд на сайте')
    prov_brand_id = models.CharField(verbose_name='ИД', max_length=255, blank=True)

    class Meta:
        unique_together = ('maker', 'name')
        verbose_name = 'Брэнд от поставщика'
        verbose_name_plural = 'Брэнды от поставщика'

    def __unicode__(self):
        return u'{} ({})'.format(self.name, self.maker)


class Category(MP_Node):

    name = models.CharField(verbose_name='Заголовок', max_length=255)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', unique=True)
    preview = models.TextField(verbose_name='Краткое описание')
    content = models.TextField(verbose_name='Описание', blank=True, null=True)
    show = models.BooleanField(verbose_name='Показывать', default=True)
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True)
    position = models.IntegerField(verbose_name='Позиция', blank=True, null=True)

    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True, null=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255, blank=True,
                                 null=True)
    metakey = models.CharField(verbose_name='Meta key', max_length=255, blank=True, null=True)
    metades = models.CharField(verbose_name='Meta des', max_length=255, blank=True, null=True)

    def getchildrens(self):
        return Category.get_children(self).filter(show=True)

    def save(self, **kwargs):
        if not self.id:
            self.slug_title = slugify(self.slug_title)
        super(Category, self).save(**kwargs)

    class Meta:
        verbose_name = 'Категория на сайте'
        verbose_name_plural = 'Категории на сайте'

    def __unicode__(self):
        return u'{}{}'.format((self.depth - 1) * u'---', self.name)


class CategoryXML(MP_Node):

    def default_cat_id(self):
        return hashlib.md5(slugify(self.name)).hexdigest()

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    name = models.CharField(verbose_name='Заголовок', max_length=255, blank=False)
    cat_id = models.CharField(verbose_name='ИД', max_length=100)
    category = models.ForeignKey(Category, verbose_name='Категория на сайте',
                                 blank=True, null=True, related_name='categorys_xml')
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

    def __unicode__(self):
        return u'{}{} ({})'.format((self.depth - 1) * u'---', self.name, self.maker)


class Status(models.Model):

    name = models.CharField(verbose_name='Статус', max_length=255, unique=True)
    official = models.CharField(verbose_name='Наименование статуса', max_length=255)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __unicode__(self):
        return self.official


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
        return u'{} ({})'.format(self.name, self.maker)


class Tovar(models.Model):

    def upload_path(self, path):
        return os.path.join('upload_tovar', self.maker.name, '{}{}'.
                            format(hashlib.md5(slugify(self.name)).hexdigest(), '.jpg'))

    def default_slug_title(self):
        return slugify(u'{}_{}_{}'.format(self.maker, self.name, self.code))[:255]

    def default_code(self):
        return hashlib.md5(slugify(self.name)).hexdigest()

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    name = models.CharField(verbose_name='Заголовок', max_length=255, blank=False)
    product_id = models.CharField(verbose_name='ИД', max_length=50, blank=True)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', max_length=255,
                                  blank=True, unique=True)
    code = models.CharField(verbose_name='Артикул', max_length=50, blank=True)
    content = models.TextField(verbose_name='Описание', blank=True)
    long_content = models.TextField(verbose_name='Полное описание', blank=True)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=10, null=True)
    stock = models.IntegerField(verbose_name='Остаток', null=True, blank=True, default=None)
    size = models.CharField(verbose_name='Размеры', max_length=256, blank=True)
    material = models.CharField(verbose_name='Материал', max_length=128, blank=True)

    small_image = models.ImageField(verbose_name='Путь к файлу картинки 200х200',
                                    blank=True, max_length=255, upload_to=upload_path)
    big_image = models.ImageField(verbose_name='Путь к файлу картинки 280х280',
                                  blank=True, max_length=255, upload_to=upload_path)
    super_big_image = models.ImageField(verbose_name='Путь к файлу картинки 1000х1000',
                                        blank=True, max_length=255, upload_to=upload_path)
    brand = ChainedForeignKey(BrandMaker,
                              chained_field='maker',
                              chained_model_field='maker',
                              show_all=False,
                              auto_choose=False,
                              verbose_name='Брэнд',
                              blank=True,
                              null=True)
    status = models.ForeignKey(Status, verbose_name='Статус', blank=True, null=True)
    categoryxml = models.ManyToManyField(CategoryXML, verbose_name=u'Категория для товара', blank=True)
    print_type = models.ManyToManyField(PrintType, verbose_name=u'Нанесение для товара', blank=True)
    show = models.BooleanField(verbose_name='Показывать', default=True)

    content_seo = models.TextField(verbose_name='Описание для SEO', blank=True)
    title_seo = models.CharField(verbose_name='Заголовок для SEO', max_length=255, blank=True)
    metakey = models.CharField(verbose_name='Meta key', max_length=255, blank=True)
    metades = models.CharField(verbose_name='Meta des', max_length=255, blank=True)

    import_fl = models.BooleanField(verbose_name='Импортирован в базу', default=False)

    def photos(self):
        return TovarAttachment.objects.filter(tovar=self, meaning=1)

    def get_type(self):
        return 1

    def save(self, **kwargs):
        if not self.id and not self.import_fl:
            self.code = self.default_code()
            self.slug_title = self.default_slug_title()
        super(Tovar, self).save()

    class Meta:
        unique_together = ('maker', 'code')
        ordering = ('price',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __unicode__(self):
        return self.name


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
    def default_code(self):
        return hashlib.md5(slugify(self.name)).hexdigest()

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    tovar = models.ForeignKey(Tovar, verbose_name='Товар')

    name = models.CharField(verbose_name='Заголовок', max_length=255)
    code = models.CharField(verbose_name='Артикул', max_length=50)
    product_id = models.CharField(verbose_name='ИД', max_length=50)
    main_product_id = models.CharField(verbose_name='ИД родителя', max_length=50)

    params = models.CharField(verbose_name='Доп.параметры', max_length=255)
    stock = models.IntegerField(verbose_name='Остаток', null=True, blank=True,
                                default=None)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2,
                                max_digits=10, null=True)

    def get_type(self):
        return 0

    def save(self, **kwargs):
        if not self.id:
            self.code = self.code or self.default_code()
        self.maker = self.tovar.maker
        super(SubTovar, self).save()

    class Meta:
        unique_together = ('maker', 'code')
        verbose_name = 'Вариант товара'
        verbose_name_plural = 'Варианты товаров'

    def __unicode__(self):
        return self.name


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
    def upload_path(self, path):
        return os.path.join('upload_attachment', self.maker.name, '{}{}'.
                            format(hashlib.md5(slugify(self.name)).hexdigest(), '.jpg'))

    MEANINGS = (
        (0, 'Изображение'),
        (1, 'Файл')
    )

    maker = models.ForeignKey(Maker, verbose_name='Поставщик')
    tovar = models.ForeignKey(Tovar, verbose_name='Товар')
    meaning = models.IntegerField(verbose_name='Тип файла', choices=MEANINGS)
    file = models.FileField(verbose_name='URL доп.файла', upload_to=upload_path,
                            blank=True)
    image = models.ImageField(verbose_name='URL доп.картинки', upload_to=upload_path,
                              blank=True)
    name = models.CharField(verbose_name='Описание доп.файла или картинки', max_length=255)

    def save(self, **kwargs):
        self.maker = self.tovar.maker
        super(TovarAttachment, self).save()

    class Meta:
        unique_together = ('tovar', 'image', 'file')
        verbose_name = 'Дополнительный файл (изображение)'
        verbose_name_plural = 'Дополнительные файлы (изображения)'

    def __unicode__(self):
        return self.name


class MSettings(models.Model):

    title = models.CharField(verbose_name='Заголовок раздела', max_length=128)
    content = models.TextField(verbose_name='Контент основной страницы раздела', blank=True, null=True)

    class Meta:
        verbose_name = 'Настройка раздела Каталог'
        verbose_name_plural = 'Настройки раздела Каталог'