# coding: utf-8

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from catalog.models import PrintType


class Basket(models.Model):

    """
        Additions:
        session = models.ForeignKey(Session)
        user = models.ForeignKey(User)
    """

    creation_date = models.DateTimeField(verbose_name=u'creation date')
    checked_out = models.BooleanField(default=False, verbose_name=u'checked out')

    class Meta:
        verbose_name = u'cart'
        verbose_name_plural = u'carts'
        ordering = (u'-creation_date',)


class Item(models.Model):

    """
        Additions:
        basket = models.ForeignKey(Cart, blank=False, null=False)
        product = models.ForeignKey(Product, verbose_name='Товар', blank=False, null=False)
    """

    quantity = models.PositiveIntegerField(verbose_name='Количество', blank=True, null=True)
    unit_price = models.IntegerField(verbose_name='Цена единицы', blank=True, null=True)
    item_price = models.IntegerField(verbose_name='Цена комплекта', blank=True, null=True)
    image = models.ImageField(verbose_name='Путь к файлу картинки', blank=True,
                              null=True, max_length=255)

    class Meta:
        verbose_name = u'item'
        verbose_name_plural = u'items'
        ordering = (u'cart',)
