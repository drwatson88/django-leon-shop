# coding: utf-8


from django.forms import forms, fields


class ShopDeliveryServiceForm(forms.Form):

    pass


class ShopBaseContactForm(forms.Form):

    pass


class ShopShortContactForm(ShopBaseContactForm):

    pass


class ShopCourierContactForm(ShopShortContactForm):

    pass


class ShopFullContactForm(ShopCourierContactForm):

    pass


class ShopPaymentForm(forms.Form):

    is_prepaid = fields.CharField(required=False, widget=fields.HiddenInput)
    step_name = u'Выберите способ оплаты'


class ShopConfirmForm(forms.Form):

    step_name = u'Подтвердите заказ'


