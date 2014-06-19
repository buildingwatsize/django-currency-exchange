#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-currency-exchange',
    version='0.1.0',
    description='Django Foreign Exchange',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/django-currency-exchange',
    packages=find_packages(),
    install_requires=['django', 'requests']
)
