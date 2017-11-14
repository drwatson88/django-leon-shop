# -*- coding: utf-8 -*-

import os

from treebeard.mp_tree import MP_Node
from pytils.translit import slugify
import hashlib

from django.db import models

from leon.apps.base.models import BaseStatusMixin


class ShopMaker(models.Model):

    title = models.CharField(verbose_name='Наименование поставщика', max_length=255)
    code = models.CharField(verbose_name='Уникальный идентификатор', max_length=255, unique=True)

    def save(self, **kwargs):
        if not self.id:
            self.name = slugify(self.title)
        super(ShopMaker, self).save(**kwargs)

    class Meta:
        abstract = True
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.title


class ShopBrand(models.Model):
    title = models.CharField(verbose_name='Наименование бренда', max_length=255)
    code = models.CharField(verbose_name='Уникальный идентификатор', max_length=255, unique=True)

    def save(self, **kwargs):
        if not self.id:
            self.name = slugify(self.title)
        super(ShopBrand, self).save(**kwargs)

    class Meta:
        abstract = True
        verbose_name = 'Бренд на сайте'
        verbose_name_plural = 'Бренд на сайте'

    def __str__(self):
        return self.title


class ShopBrandMaker(models.Model):
    """
    Additions:
        maker = models.ForeignKey(Maker, verbose_name='Поставщик')
        brand = models.ForeignKey(ShopBrand, verbose_name='Бренд на сайте', null=True, blank=True)
        
        unique_together = ('maker', 'title')
    """
    title = models.CharField(verbose_name='Наименование', max_length=255, blank=True)
    code = models.CharField(verbose_name='Код', max_length=255, blank=True)
    prov_brand_id = models.CharField(verbose_name='ИД', max_length=255, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Брэнд от поставщика'
        verbose_name_plural = 'Брэнды от поставщика'

    def __str__(self):
        return u'{} ({})'.format(self.title, self.maker)


class ShopCategorySite(MP_Node):

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', unique=True, blank=True)
    preview = models.TextField(verbose_name='Краткое описание', blank=True, null=True)
    content = models.TextField(verbose_name='Описание', blank=True, null=True)
    show = models.BooleanField(verbose_name='Показывать', default=True)
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True)
    position = models.IntegerField(verbose_name='Позиция', blank=True, null=True)

    def get_absolute_url(self):
        pass

    def get_children(self):
        return super(ShopCategorySite, self).get_children().filter(show=True)

    def save(self, **kwargs):
        if not self.id:
            self.slug_title = slugify(self.title)
        super(ShopCategorySite, self).save(**kwargs)

    class Meta:
        abstract = True
        verbose_name = 'Категория на сайте'
        verbose_name_plural = 'Категории на сайте'

    def __str__(self):
        return '{}{}'.format((self.depth - 1) * '---', self.slug_title)


class ShopCategoryXML(MP_Node, BaseStatusMixin):
    """
    Additions:
        maker = models.ForeignKey(Maker, verbose_name='Поставщик')
        category_site = models.ForeignKey(CategorySite, verbose_name='Категория на сайте',
                                          blank=True, null=True, related_name='category_xml_s')
        filters = models.ManyToManyField(Filter, verbose_name='Фильтры', related_name='category')
                                          
        unique_together = ('maker', 'cat_id')
    """

    def default_cat_id(self):
        return hashlib.md5(slugify(self.title).encode(encoding='utf-8')).hexdigest()

    title = models.CharField(verbose_name='Заголовок', max_length=255, blank=False)
    cat_id = models.CharField(verbose_name='ИД', max_length=100)
    import_fl = models.BooleanField(verbose_name='Импортирован в базу', default=False)

    class Meta:
        abstract = True
        verbose_name = 'Категория от поставщика'
        verbose_name_plural = 'Категории от поставщиков'

    def save(self, **kwargs):
        if not self.id and not self.import_fl:
            self.cat_id = self.default_cat_id()
        super(ShopCategoryXML, self).save()

    def __str__(self):
        return u'{}{} ({})'.format((self.depth - 1) * u'---', self.title, self.maker)


class ShopProduct(models.Model):
    """
    Additions:
        maker = models.ForeignKey(Maker, verbose_name='Поставщик')
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
                                         
        unique_together = ('maker', 'code')
    """

    def default_slug_title(self):
        return slugify('{}_{}_{}'.format(self.maker, self.title, self.code))[:255]

    def default_code(self):
        return hashlib.md5(slugify(self.title).encode(encoding='utf-8')).hexdigest()

    def product_upload_path(self, instance):
        return os.path.join('upload_product', self.maker.name, '{}{}'.
                            format(hashlib.md5(slugify(self.title).
                                               encode(encoding='utf-8')).hexdigest(), '.jpg'))

    parent = models.ForeignKey("self", verbose_name='Основной продукт', blank=True, null=True,
                               on_delete=models.CASCADE, related_name='children_set')
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
    show = models.BooleanField(verbose_name='Показывать', default=True)
    import_fl = models.BooleanField(verbose_name='Импортирован в базу', default=False)

    def get_price(self):
        pass

    def get_price_with_discount(self):
        pass

    def get_discount(self):
        pass

    def get_children_s(self):
        return self.children_set

    def photo_s(self):
        return self.attachment.filter(meaning=1).order_by('position').all()

    def main_image(self):
        return self.attachment.filter(meaning=1).order_by('position').first()

    def save(self, **kwargs):
        if not self.id and not self.import_fl:
            self.code = self.code or self.default_code()
            self.slug_title = self.default_slug_title()
        super(ShopProduct, self).save()

    class Meta:
        abstract = True
        ordering = ('price',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class ShopProductPackKV(models.Model):
    """
    Additions:
        maker = models.ForeignKey(Maker, verbose_name='Поставщик')
        product = models.ForeignKey(Product, verbose_name='Товар')
        
        unique_together = ('product', 'pack_id', 'abbr')
    """

    pack_id = models.IntegerField(verbose_name='Порядковый номер пакета у товара',
                                  default=0)
    abbr = models.CharField(verbose_name='Название поля (поиск)', max_length=255)
    name = models.CharField(verbose_name='Имя поля', max_length=255)
    value = models.CharField(verbose_name='Значение поля', max_length=255)
    position = models.IntegerField(verbose_name='Порядок', null=True)

    class Meta:
        abstract = True


class ShopProductStock(models.Model):
    """
    Additions:
        maker = models.ForeignKey(Maker, verbose_name='Поставщик')
        product = models.ForeignKey(Product, verbose_name='Товар')
        
        unique_together = ('product', 'abbr')
    """

    geo = models.CharField(verbose_name='ГеоМетка', max_length=100)
    type = models.CharField(verbose_name='Тип', max_length=255)
    value = models.IntegerField(verbose_name='Значение поля')

    class Meta:
        abstract = True


class ShopProductParamsKV(models.Model):
    """
    Additions:
        product = models.ForeignKey(Product, verbose_name='Товар', related_name='params_kv')
        
        unique_together = ('product', 'abbr')
    """

    code = models.CharField(verbose_name='Код поля', max_length=255)
    title = models.CharField(verbose_name='Имя поля', max_length=255)
    value = models.CharField(verbose_name='Значение поля', max_length=4000)
    value_hash = models.IntegerField(verbose_name='Хэш значение поля')
    position = models.IntegerField(verbose_name='Порядок', null=True)

    class Meta:
        abstract = True


class ShopProductAttachment(models.Model):
    """
    Additions:
        product = models.ForeignKey(Product, verbose_name='Товар', related_name='attachment')
    """

    MEANINGS = (
        (0, 'Изображение'),
        (1, 'Файл')
    )

    def product_attachment_upload_path(self):
        return os.path.join('upload_attachment', self.maker.name, '{}{}'.
                            format(hashlib.md5(slugify(self.desc).
                                               encode(encoding='utf-8')).hexdigest(), '.jpg'))

    meaning = models.IntegerField(verbose_name='Тип файла', choices=MEANINGS)
    href = models.ImageField(verbose_name='URL картинки',
                             upload_to=product_attachment_upload_path,
                             blank=True)
    type = models.CharField(verbose_name='Тип', max_length=20)
    desc = models.CharField(verbose_name='Описание', max_length=255)
    position = models.IntegerField(verbose_name='Порядок', null=True)

    def save(self, **kwargs):
        self.maker = self.product.maker
        super(ShopProductAttachment, self).save()

    def __str__(self):
        return self.desc

    class Meta:
        abstract = True
        verbose_name = 'Файл (изображение)'
        verbose_name_plural = 'Файлы (изображения)'


class ShopFilter(models.Model):
    """
    Additions:
        category_site = models.ForeignKey(CategorySite, verbose_name='Категория на сайте',
                                          blank=True, null=True, related_name='category_xml_s')

        unique_together = ('category_site', 'type', 'code')
    """

    TYPE_CHOICES = (
        ('FIELD', 'Поле'),
        ('M2M', 'Многие-ко-многим (доп.класс)'),
        ('FK', 'Один-ко-многим (доп.класс)'),
        ('KV', 'Хранилище доп. параметров'),
    )

    title = models.CharField(verbose_name='Название фильтра', max_length=255)
    code = models.CharField(verbose_name='Наименование фильтра', max_length=255)
    type = models.CharField(verbose_name='Значение поля фильтра', choices=TYPE_CHOICES, max_length=50)
    kv_key = models.CharField(verbose_name='Ключ фильтра', max_length=50, null=True, blank=True)
    field_name = models.CharField(verbose_name='Название поля', max_length=50, null=True, blank=True)
    unit = models.CharField(verbose_name='Единица измерения', max_length=10, null=True, blank=True)
    query_method = models.CharField(verbose_name='Метод фильтра', max_length=50, null=True, blank=True)
    template = models.CharField(verbose_name='Шаблон реализации', max_length=50, null=False, blank=False)
    position = models.IntegerField(verbose_name='Позиция в списке')

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'


class ShopOrderReference(models.Model):

    code = models.CharField(verbose_name='Тип порядка сортировки продукта',
                            max_length=255, unique=True)
    title = models.CharField(verbose_name='Наименование типа порядка'
                                          'сортировки продукта', max_length=255)
    field_name = models.CharField(verbose_name='Поле сортировки продукта', max_length=30)
    field_order = models.BooleanField(verbose_name='Порядок сортировки')
    position = models.IntegerField(verbose_name='Позиция в списке')

    class Meta:
        abstract = True
        verbose_name = 'Тип порядка сортировки продукта'
        verbose_name_plural = 'Типы порядков сортировки продукта'


class Settings(models.Model):

    title = models.CharField(verbose_name='Заголовок раздела', max_length=128)
    content = models.TextField(verbose_name='Контент основной страницы раздела',
                               blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = 'Настройка раздела Каталог'
        verbose_name_plural = 'Настройки раздела Каталог'
