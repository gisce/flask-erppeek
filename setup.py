#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='flask-erppeek',
    version='1.0.0',
    url='https://github.com/gisce/flask-erppeek',
    license='BSD',
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    description='ERPPeek Connector for Flask',
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'erppeek'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
