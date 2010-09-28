#!/usr/bin/env python

import sys, os
from distutils.core import setup
from as2dh import get_version

version = get_version()

data = dict(
    name =          'as2dh',
    version =       version,
    url =           'http://blog.lunar-dev.net',
    download_url =  '',
    description =   'An AsDoc to Devhelp converter.',
    author =        'Vincent Petithory',
    author_email =  'vincent [dot] petithory [at] gmail.com',
    maintainer =    'Vincent Petithory',
    maintainer_email = 'vincent [dot] petithory [at] gmail.com',
    license =       'GPL License',
    packages =      ['as2dh'],
    scripts =       ['bin/as2dh'],
    cmdclass =      {},
    classifiers =   ['Development Status :: 5 - Production/Stable',
                     'License :: OSI Approved :: GPL License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2',
                     'Programming Language :: Python :: 2.3',
                     'Programming Language :: Python :: 2.4',
                     'Programming Language :: Python :: 2.5',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.0',
                     'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                     'Topic :: Software Development :: Documentation',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Topic :: Text Processing :: Filters',
                     'Topic :: Text Processing :: Markup :: HTML',
                    ],
    ) 

setup(**data)
