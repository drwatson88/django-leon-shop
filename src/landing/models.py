# coding: utf-8


from django.db import models


class ShopLanding(models.Model):

    template = models.CharField(verbose_name='Шаблон', max_length=250)
    slug_title = models.SlugField(verbose_name='Имя для ссылки', unique=True, blank=True,
                                  null=True, max_length=150)

    class Meta:
        abstract = True
        verbose_name = u'Шаблон для лэндинга'
        verbose_name_plural = u'Шаблоны для лэндинга'
