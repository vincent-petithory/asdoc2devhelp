#!/usr/bin/env python
#-*- coding:utf-8 -*-

import as2dh.dist
import os

ASDOCS_PATH = '%s/asdocs' % os.getcwd()

# asdocs
as3_gettext = dict(
    asdoc_path = '%s/as3-gettext-0.5' % ASDOCS_PATH,
    title = 'AS3 GNU Gettext API Reference',
    name = 'as3-gettext-0.5',
    prefix = os.path.expanduser('~/.local'),
    is_dry_run = False,
)

as3_langref = dict(
    asdoc_path = '%s/AS3LR' % ASDOCS_PATH,
    title = 'AS3 Language API Reference',
    name = 'as3_langref',
    prefix = os.path.expanduser('~/.local'),
    is_dry_run = False,
)

as2dh.dist.install(**as3_gettext)
as2dh.dist.install(**as3_gettext)
#as2dh.dist.uninstall(**as3_gettext)
#as2dh.dist.uninstall(**as3_gettext)
