#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requirements = [
    'Jinja2',
    'beautifulsoup4',
    'requests'
]

setup(
    name='niftyhacks',
    version='0.3.0',
    description='assorted hacks by @anandology',
    author='Anand Chitipothu',
    author_email='anandology@gmail.com',
    url='https://github.com/anandology/niftyhacks',
    packages=[
        'niftyhacks',
    ],
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points='''
        [console_scripts]
        jinja-envy=niftyhacks.jinja_envy:main
    '''
)
