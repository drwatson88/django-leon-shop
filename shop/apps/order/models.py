# coding: utf-8


from django.db import models


class ShopDeliveryCompany(models.Model):

    name = models.CharField(verbose_name='Название компании', max_length=250)
    code = models.CharField(verbose_name='ID компании', max_length=100)

    class Meta:
        abstract = True
        verbose_name = u'Компания доставки'
        verbose_name_plural = u'Компании доставки'


class ShopDeliveryCity(models.Model):

    name = models.CharField(verbose_name='Название города', max_length=250)
    kladr = models.CharField(verbose_name='ФИАС', max_length=15)
    fias = models.CharField(verbose_name='ФИАС', max_length=15)
    address = models.CharField(verbose_name='Адрес', max_length=250)

    class Meta:
        abstract = True
        verbose_name = u'Город'
        verbose_name_plural = u'города'


class ShopOrder(models.Model):

    """
    Additions:
        basket = models.ForeignKey(Cart, blank=False, null=False)
        product = models.ForeignKey(Product, verbose_name='Товар', blank=False, null=False)
    """

    first_name = models.CharField(verbose_name='Имя')
    middle_name = models.CharField(verbose_name='Отчество')
    last_name = models.CharField(verbose_name='Фамилия')

    email = models.CharField(verbose_name='Почта')
    phone = models.CharField(verbose_name='Телефон')

    region = models.CharField(verbose_name='Регион')
    area = models.CharField(verbose_name='Область')
    city = models.CharField(verbose_name='Город')
    settlement = models.CharField(verbose_name='Поселок/деревня')
    street = models.CharField(verbose_name='Улица')
    house = models.CharField(verbose_name='Дом')
    flat = models.CharField(verbose_name='Квартира')

    class Meta:
        abstract = True
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'
