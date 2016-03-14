# -*- coding: utf-8 -*-

from django import forms
from .models import Maker


class Mixin(object):
    def __init__(self, data=None, *args, **kwargs):
        super(Mixin, self).__init__(data, *args, **kwargs)
        for k, field in self.fields.items():
            if u'required' in field.error_messages:
                field.error_messages[u'required'] = u'Заполните поле {0:s}.'.format(field.label)
            if u'invalid' in field.error_messages:
                field.error_messages[u'invalid'] = u"Неправильно заполнено поле {0:s}.".format(field.label)


class TovarFormFilter(Mixin, forms.Form):

    # maker = forms.ModelChoiceField(queryset=Maker.objects.all(), empty_label=None)
    makers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label=u'')
    price_fr = forms.IntegerField(max_value=1000000, min_value=0)
    price_to = forms.IntegerField(max_value=1000000, min_value=1)