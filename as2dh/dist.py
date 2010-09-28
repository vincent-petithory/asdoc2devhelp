#!/usr/bin/env python
#-*- coding:utf-8 -*-

import as2dh
import os
import shutil
import sys

def install(asdoc_path, title, name, prefix, is_dry_run = False):
    if not os.path.exists(asdoc_path):
        sys.stderr.write('%s does not exist.\n' % asdoc_path)
        return 1
    # check the given prefix is valid
    if not os.path.exists(prefix):
        sys.stderr.write('%s prefix does not exist.\n' % prefix)
        return 1
    
    asdoc_dist_path = install_asdoc_content(asdoc_path, prefix, is_dry_run)
    install_devhelp_file(asdoc_dist_path, title, name, prefix, is_dry_run)

def install_asdoc_content(asdoc_path, prefix, is_dry_run = False):
    book_name = os.path.basename(asdoc_path)
    # Make asdoc directory if necessary
    share_doc_path = '%s/share/doc' % prefix
    if not os.path.exists(share_doc_path):
        os.makedirs(share_doc_path)
    # remote existing asdoc
    asdoc_dist_path = '%s/%s' % (share_doc_path, book_name)
    if os.path.exists(asdoc_dist_path):
        shutil.rmtree(asdoc_dist_path)
    # copy asdoc content
    shutil.copytree(asdoc_path, asdoc_dist_path)
    return asdoc_dist_path

def install_devhelp_file(asdoc_path, title, name, prefix, is_dry_run = False):
    book_name = os.path.basename(asdoc_path)
    # Make devhelp content
    asdoc = as2dh.Asdoc(asdoc_path)
    dh = as2dh.Devhelp(asdoc, title, name)
    devhelp2_content = dh.get_xml()
    
    # Make devhelp directory if necessary
    devhelp_books_path = '%s/share/devhelp/books' % prefix
    devhelp_file_path = '%s/%s/%s.devhelp2' % (devhelp_books_path, book_name, book_name)
    devhelp_dir_path = os.path.dirname(devhelp_file_path)
    if not os.path.exists(devhelp_dir_path):
        os.makedirs(devhelp_dir_path)
    
    # Write the devhelp file
    devhelp_file = open(devhelp_file_path, 'wb')
    devhelp_file.write(devhelp2_content)
    devhelp_file.close()
    return devhelp_file_path

def uninstall(book_name, prefix, is_dry_run = False):
    asdoc_path = '%s/share/doc/%s' % (prefix, book_name)
    devhelp_book_path = '%s/share/devhelp/books/%s' % (prefix, book_name)
    if os.path.exists(asdoc_path):
        shutil.rmtree(asdoc_path)
    if os.path.exists(devhelp_book_path):
        shutil.rmtree(devhelp_book_path)
