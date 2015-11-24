#!/usr/bin/env python

from setuptools import setup

PACKAGE = 'TracHtAndDokuPasswdStore'

setup(
    name=PACKAGE,
    version='0.5',
    description='AccountManager Trac plugin module for authentication with htpasswd files and dokuwiki users. It does not allow to add/remove/change users',
    author='Luca Ferroni',
    author_email='luca@befair.it',
    packages=['htanddokupasswdstore'],
    license='AGPLv3',
    keywords='trac plugin accountmanager dokuwiki htpasswd',
    url='https://github.com/feroda/htanddokupasswdstore',
    classifiers=[
        'Framework :: Trac',
    ],
    install_requires=['TracAccountManager'],
    entry_points={
        'trac.plugins': [
            '%s = htanddokupasswdstore.htfileanddokuauth' % PACKAGE,
        ]
    },
)
