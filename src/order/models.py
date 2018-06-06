# coding: utf-8


from datetime import datetime
from django.db import models
from leon.apps.base.models import BaseUidMixin, BaseStatusMixin, BasePositionMixin


class ShopDeliveryCompany(BaseUidMixin, BaseStatusMixin, BasePositionMixin):

    title = models.CharField(verbose_name='Название компании', max_length=250)
    code = models.CharField(verbose_name='ID компании', max_length=100)

    class Meta:
        abstract = True
        verbose_name = u'Компания доставки'
        verbose_name_plural = u'Компании доставки'


class ShopDeliveryCity(BaseUidMixin, BaseStatusMixin, BasePositionMixin):

    name = models.CharField(verbose_name='Название города', max_length=250)
    kladr = models.CharField(verbose_name='ФИАС', max_length=15, null=True, blank=True)
    fias = models.CharField(verbose_name='ФИАС', max_length=15, null=True, blank=True)
    address = models.CharField(verbose_name='Адрес', max_length=250, null=True, blank=True)
    index = models.CharField(verbose_name='Индекс', max_length=50, null=True, blank=True)
    is_main = models.BooleanField(verbose_name='В списке главных', default=False)

    region = models.CharField(verbose_name='Регион', max_length=50, null=True, blank=True)
    area = models.CharField(verbose_name='Область', max_length=50, null=True, blank=True)
    city = models.CharField(verbose_name='Город', max_length=50, null=True, blank=True)
    settlement = models.CharField(verbose_name='Поселок/деревня', max_length=50, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = u'Город'
        verbose_name_plural = u'Города'


class ShopDeliveryService(BaseStatusMixin):

    """
        Additions:
        company = models.ForeignKey(DeliveryCompany, verbose_name='Компания')
        city = models.ForeignKey(DeliveryCity, verbose_name='Город')
    """

    price = models.FloatField(u'Цена', null=True, blank=True)
    detail = models.TextField(u'Описание', null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = u'Сервис'
        verbose_name_plural = u'Сервисы'


class ShopOrder(models.Model):

    """
        Additions:
        session = models.ForeignKey(Session)
        user = models.ForeignKey(User)
    """

    creation_date = models.DateTimeField(verbose_name='creation date', default=datetime.now)
    checked_out = models.BooleanField(default=False, verbose_name=u'checked out')
    name = models.CharField(verbose_name='Имя', max_length=50, null=True, blank=True)

    email = models.EmailField(verbose_name='Почта', max_length=50, null=True, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=30, null=True, blank=True)
    comment = models.CharField(verbose_name='Комментарии', max_length=30, null=True, blank=True)

    is_prepaid = models.NullBooleanField(verbose_name='Предоплата', max_length=30, default=True, blank=True)

    region = models.CharField(verbose_name='Регион', max_length=50, null=True, blank=True)
    area = models.CharField(verbose_name='Область', max_length=50, null=True, blank=True)
    city = models.CharField(verbose_name='Город', max_length=50, null=True, blank=True)
    settlement = models.CharField(verbose_name='Поселок/деревня', max_length=50, null=True, blank=True)
    street = models.CharField(verbose_name='Улица', max_length=50, null=True, blank=True)
    house = models.CharField(verbose_name='Дом', max_length=10, null=True, blank=True)
    flat = models.CharField(verbose_name='Квартира', max_length=10, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ShopOrderItem(models.Model):

    """
        Additions:
        order = models.ForeignKey(Basket, blank=False, null=False, related_name='item')
        product = models.ForeignKey(Product, verbose_name='Товар', blank=False, null=False)
    """

    quantity = models.PositiveIntegerField(verbose_name='Количество', blank=True, null=True)

    @classmethod
    def add_item(cls, order, product, quantity):
        item = cls.objects.update_or_create(basket=order, product=product, quantity=quantity)
        item.save()

    def total(self):
        return self.product.price * self.quantity

    def get_image(self):
        return self.product.main_image()

    class Meta:
        abstract = True
        verbose_name = u'order item'
        verbose_name_plural = u'order items'
        ordering = (u'order',)
