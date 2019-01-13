#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Setup.

Copyright (c) 2018 Przemysław Kaliś przemek.kalis@gmail.com

"""


from setuptools import setup

setup(author='Przemek Kaliś',
      author_email='przemek.kalis@gmail.com',
      description=('(very) Simple library for keeping and manipulating'
                   + ' photometric data in LDT and IES formats.'),
      install_requires=[
        'cerberus',
        'matplotlib',
        'numpy',
      ],
      license='MIT',
      name='phfile',
      packages=['phfile'],
      url='https://github.com/przemekk1385/phfile',
      version='0.1.0',
      zip_safe=False)
