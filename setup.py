#!/usr/bin/env python

from distutils.core import setup
from setuptools import setup, find_packages

print(find_packages())

setup(
    name='django-leon-shop',
    version='0.1.1',
    description='Python E-Commerce Django Utils',
    author='Denis Sidorov',
    author_email='dvsidorov88@mail.ru',
    url='https://github.com/dvsidorov/django-leon-shop',
    packages=['shop',
              'shop.catalog',
              'shop.basket',
              'shop.order',
              'shop.search',
              'shop.landing'],
    package_dir={'shop': 'src'}
)
