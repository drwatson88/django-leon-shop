# coding: utf-8


from django.forms import forms, fields


class DeliveryCityForm(forms.Form):

    city = fields.CharField(verbose_name='Город')
