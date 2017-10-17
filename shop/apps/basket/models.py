# coding: utf-8


from django.db import models


class ShopBasket(models.Model):

    """
        Additions:
        session = models.ForeignKey(Session)
        user = models.ForeignKey(User)
    """

    creation_date = models.DateTimeField(verbose_name=u'creation date')
    checked_out = models.BooleanField(default=False, verbose_name=u'checked out')

    @classmethod
    def get_current(cls, request):
        cls.objects.filter(cls.request2filter(request))

    @classmethod
    def request2filter(cls, request):
        if request.user.is_authenticated():
            return {'user': request.user}
        elif request.session.session_key:
            return {'session_id': request.session.session_key}
        return {'user': -1}

    class Meta:
        abstract = True
        verbose_name = u'basket'
        verbose_name_plural = u'baskets'
        ordering = (u'-creation_date',)


class ShopBasketItem(models.Model):

    """
        Additions:
        basket = models.ForeignKey(Basket, blank=False, null=False)
        product = models.ForeignKey(Product, verbose_name='Товар', blank=False, null=False)
    """

    quantity = models.PositiveIntegerField(verbose_name='Количество', blank=True, null=True)
    image = models.ImageField(verbose_name='Путь к файлу картинки', blank=True,
                              null=True, max_length=255)

    @classmethod
    def add_item(cls, basket, product, quantity):
        cls.objects.update_or_create(basket=basket, product=product, quantity=quantity)

    class Meta:
        abstract = True
        verbose_name = u'basket item'
        verbose_name_plural = u'basket items'
        ordering = (u'basket',)
