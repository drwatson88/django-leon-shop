# coding: utf-8


from django.db import models


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
        verbose_name = u'order'
        verbose_name_plural = u'orders'
