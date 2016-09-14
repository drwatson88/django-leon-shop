# -*- coding: utf-8 -*-


from django import forms
from .models import CategoryXML, CategorySite, Brand, BrandMaker, PrintType, \
    PrintTypeMaker, Status, Maker


class ChangeProductCategoryXMLForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    categoryxml = forms.ModelChoiceField(queryset=CategoryXML.objects.all(),
                                         label='Категория от поставщика')


class ChangeProductPrintTypeForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    print_type = forms.ModelChoiceField(queryset=PrintTypeMaker.objects.all(),
                                        label='Вид нанесения от поставщика')


class ChangeProductBrandForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    brand = forms.ModelChoiceField(queryset=BrandMaker.objects.all(),
                                   label='Бренд от поставщика')


class ChangeProductStatusForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    status = forms.ModelChoiceField(queryset=Status.objects.all(),
                                    label='Статус')


class ChangeProductMakerForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    maker = forms.ModelChoiceField(queryset=Maker.objects.all(),
                                   label='Поставщик')


class ChangeCategoryXMLCategorySiteForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    category = forms.ModelChoiceField(queryset=CategorySite.objects.all(),
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
