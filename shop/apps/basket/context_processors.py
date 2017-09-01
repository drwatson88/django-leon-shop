# coding: utf-8

from .cart import SessionCart


def session_cart(request):
    cart = SessionCart(request)
    cart.summ = 0
    cart.coutn = 0
    cart.items_lst = list()
    for item in cart:
        cart.summ += item.quantity * item.unit_price
        cart.coutn += item.quantity

        if item.content_type.name == u'sub tovar':
            item.image = item.product.tovar.small_image
            cart.items_lst.append(item)
        else:
            item.image = item.product.small_image
            cart.items_lst.append(item)

    # import pprint as ppp
    # ppp.pprint(cart.items_lst)

    return {u'cart_header': cart,}