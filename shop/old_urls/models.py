# -*- coding: utf-8 -*-


import os
from django.db import models
from catalog.models import Category, Tovar


class CategorySiteRedirect(models.Model):
    old_slug_name = models.SlugField(unique=True)
    old_name = models.CharField(max_length=255)
    category_site = models.ForeignKey(Category, null=True)


class ProductRedirect(models.Model):
    old_maker_id = models.IntegerField()
    old_code = models.CharField(max_length=255)
    old_slug_name = models.SlugField(unique=True)
    old_name = models.CharField(max_length=255)
    product = models.ForeignKey(Tovar, null=True)
