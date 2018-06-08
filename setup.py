#!/usr/bin/env python

from distutils.core import setup


setup(
    name='django-leon-shop',
    version='0.1.1',
    description='Python E-Commerce Django Utils',
    author='Denis Sidorov',
    author_email='dvsidorov88@mail.ru',
    url='https://github.com/dvsidorov/django-leon-shop',
    packages=['leon_shop',
              'leon_shop.catalog',
              'leon_shop.basket',
              'leon_shop.order',
              'leon_shop.search',
              'leon_shop.landing'],
    package_dir={'leon_shop': 'src'}
)
