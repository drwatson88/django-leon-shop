# -*- coding: utf-8 -*-


from django import forms
from models import CategoryXML


class TovarForm(forms.ModelForm):
    model = CategoryXML

    def __init__(self, *args, **kwargs):
        super(TovarForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['categoryxml'].queryset = CategoryXML.objects. \
                filter(maker=kwargs['initial']['maker'])
