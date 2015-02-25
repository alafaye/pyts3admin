#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup


setup(
    name = 'pyts3admin',
    version = '0.1.0',
    description = 'An ts3 administration tool',
    long_description = open('README.rst').read(),
    author = 'Alexandre Lafaye',
    author_email = 'lafa.alexandre@gmail.com',
    url = 'https://github.com/alafaye/pyts3admin',
    packages = ['pyts3admin'],
    install_requires = ['pyts3'],
    requires = ['pyts3'],
    license = "None",
    keywords = 'ts3 administration',
    platforms = 'any',
    classifiers = [
        'Topic :: Server Administration',
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independant',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
