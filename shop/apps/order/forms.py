# coding: utf-8


from django.forms import forms, fields


class ShopDeliveryCityServiceForm(forms.Form):

    pass


class ShopBaseContactForm(forms.Form):

    pass


class ShopShortContactForm(ShopBaseContactForm):

    pass


class ShopCourierContactForm(ShopShortContactForm):

    pass


class ShopFullContactForm(ShopCourierContactForm):

    pass
