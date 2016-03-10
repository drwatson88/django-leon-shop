# -*- coding: utf-8 -*-


from django import forms
from models import CategoryXML, Category, Brand, BrandMaker, PrintType, \
    PrintTypeMaker, Status, Maker


class ChangeTovarCategoryXMLForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    categoryxml = forms.ModelChoiceField(queryset=CategoryXML.objects.all(),
                                         label='Категория от поставщика')


class ChangeTovarPrintTypeForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    print_type = forms.ModelChoiceField(queryset=PrintTypeMaker.objects.all(),
                                        label='Вид нанесения от поставщика')


class ChangeTovarBrandForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    brand = forms.ModelChoiceField(queryset=BrandMaker.objects.all(),
                                   label='Бренд от поставщика')


class ChangeTovarStatusForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    status = forms.ModelChoiceField(queryset=Status.objects.all(),
                                    label='Статус')


class ChangeTovarMakerForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    maker = forms.ModelChoiceField(queryset=Maker.objects.all(),
                                   label='Поставщик')


class ChangeCategoryXMLCategoryForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      label='Категория на сайте')


class ChangeCategoryXMLMakerForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    maker = forms.ModelChoiceField(queryset=Maker.objects.all(),
                                   label='Поставщик')


class ChangeBrandMakerBrandForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(),
                                   label='Бренд на сайте')


class ChangePrintTypeMakerPrintTypeForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    print_type = forms.ModelChoiceField(queryset=PrintType.objects.all(),
                                        label='Вид нанесения на сайте')
