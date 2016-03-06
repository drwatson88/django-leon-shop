# -*- coding: utf-8 -*-


from django import forms
from models import CategoryXML, PrintTypeMaker, Category, Brand, PrintType


class ChangeTovarCategoryXMLForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    categoryxml = forms.ModelChoiceField(queryset=CategoryXML.objects.all(),
                                         label='Категория от поставщика')


class ChangeTovarPrintTypeForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    print_type = forms.ModelChoiceField(queryset=PrintTypeMaker.objects.all(),
                                        label='Вид нанесения от поставщика')


class ChangeCategoryXMLCategoryForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      label='Категория на сайте')


class ChangeBrandMakerBrandForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(),
                                   label='Бренд на сайте')


class ChangePrintTypeMakerPrintTypeForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    print_type = forms.ModelChoiceField(queryset=PrintType.objects.all(),
                                        label='Вид нанесения на сайте')
