#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import string

"""
    Liste des packages
    Liste des classes
"""

"""
    Version info
"""

version = (0,1,0)

def get_version():
    return '.'.join(str(i) for i in version)

"""
    ASDOC tree analysis
"""


class Asdoc():
    
    CLASS_SUMMARY = 'class-summary.html'
    PACKAGE_SUMMARY = 'package-summary.html'
    INDEX_LIST = 'index-list.html'
    INDEX = 'index.html'
    
    ALL_INDEX_PATTERN = 'all-index-%s.html'
    PACKAGE_DETAIL = 'package-detail.html'
    
    IGNORE_FILES = (PACKAGE_DETAIL, CLASS_SUMMARY, PACKAGE_SUMMARY, 
            INDEX_LIST, 'images', 'AC_OETags.js', 'asdoc.js', 'cookies.js', 
            'title-bar.html', 'help.js', 'override.css', 'print.css', 
            'style.css', 'package-frame.html', 'class-list.html', 
            'package-list.html', 'package.html', 'index.html', 'all-classes.html')
    
    @staticmethod
    def __get_node_name(node):
        return node[0:node.find('.')]
    
    def __init__(self, directory_path, ignore_list = (), extra_files = ()):
        self.__directory_path = os.path.abspath(directory_path)
        self.__indexes = tuple(Asdoc.ALL_INDEX_PATTERN % 
                letter for letter in string.ascii_uppercase)
        self.__ignore_list = Asdoc.IGNORE_FILES + ignore_list + self.__indexes
        self.__extra_files = extra_files
    
    def get_root_path(self):
        return self.__directory_path
    
    def parse_asdoc(self):
        packages = []
        extras = []
        self.__parse_nodes_in_directory(self.__directory_path, packages, extras)
        
        indexes = tuple(Index(idx, Asdoc.__get_node_name(idx)) for idx in self.__indexes)
        classes = []
        for pkg in packages:
            classes.extend(pkg.elements)
        
        # TODO make the keyword list
        keywords = ()
        return (packages, classes, indexes, extras, keywords)
    
    def __get_relative_path(self, path):
        return path[path.find(self.__directory_path)+len(self.__directory_path)+1:]
    
    def __get_node_path(self, directory, node):
        return self.__get_relative_path('%s/%s' % (directory, node))
    
    def __parse_nodes_in_directory(self, directory, packages, extras):
        subfolders = []
        elements = []
        # flag for package.html presence
        dir_files = os.listdir(directory)
        is_package = Asdoc.PACKAGE_DETAIL in dir_files
            
        for node in dir_files:
            if node not in self.__ignore_list:
                if node in self.__extra_files:
                    extra = Extra(self.__get_node_path(directory, node), Asdoc.__get_node_name(node))
                    extras.append(extra)
                elif node.endswith('.html'):
                    el = Element(self.__get_node_path(directory, node), Asdoc.__get_node_name(node), None)
                    elements.append(el)
                elif node.find('.') == -1:
                    subfolders.append(node)
                    
                
        if is_package:
            package_uri = self.__get_node_path(directory, Asdoc.PACKAGE_DETAIL)
            package_name = self.__get_relative_path(directory).replace('/', '.')
            if package_name == '':
                package_name = 'Top Level'
            packages.append(Package(package_uri, package_name, elements))
        
        for folder in subfolders:
            self.__parse_nodes_in_directory(directory+'/'+folder, packages, extras)


"""
    Element classes
"""


class Package():
    
    TOP_LEVEL = 'Top Level'
    
    def __init__(self, uri, name, elements):
        self.uri = uri
        self.name = name
        self.elements = elements
        for element in self.elements:
            element.package = self
        
    
    def get_qname(self):
        if self.name == Package.TOP_LEVEL:
            return ''
        else:
            return self.name
    
    def __str__(self):
        return self.name


class Element():
    
    def __init__(self, uri, name, package):
        self.uri = uri
        self.name = name
        self.package = package
    
    def get_qname(self):
        return '%s.%s' % (self.package.get_qname(), self.name)
    
    def __str__(self):
        return self.get_qname()


class Index():
    
    def __init__(self, uri, name):
        self.uri = uri
        self.name = name
    
    def __str__(self):
        return self.name


class Extra():
    
    def __init__(self, uri, name):
        self.uri = uri
        self.name = name
    
    def __str__(self):
        return self.name

class Keyword():
    
    def __init__(self, uri, type, name):
        self.uri = uri
        self.type = type
        self.name = name


"""
    Devhelp xml writer
"""


class Devhelp():
    
    XMLNS = 'http://www.devhelp.net/book'
    LANGUAGE = 'Actionscript 3.0'
    VERSION = 2
    
    def __init__(self, asdoc, title, name, asdoc_dir = None):
        self.__asdoc = asdoc
        self.title = title
        self.name = name
        self.asdoc_dir = asdoc_dir
    
    def __make_sub(self, name, link, self_close = False):
        sub = '<sub name="%s" link="%s"' % (name, link)
        if not self_close:
            return sub+">\n%s\n</sub>"
        else:
            return sub+'/>'
    
    def get_xml(self):
        (pkgs, classes, indexes, extras, keywords) = self.__asdoc.parse_asdoc()
        root_path = self.asdoc_dir
        if root_path is None:
            root_path = self.__asdoc.get_root_path()
        
        package_summary = Asdoc.PACKAGE_SUMMARY
        class_summary = Asdoc.CLASS_SUMMARY
        index_list = Asdoc.INDEX_LIST
        index_link = Asdoc.INDEX
        
        # Header
        xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
        
        # Chapters
        
        ## packages
        xml_pkg_root = ''
        if len(pkgs) > 0:
            xml_pkg_root = self.__make_sub('Packages', package_summary, False)
            xml_pkgs = []
            for pkg in pkgs:
                xml_pkgs.append(self.__make_sub(pkg.name, pkg.uri, True))
            
            xml_pkg_root = xml_pkg_root % "\n".join(xml_pkg for xml_pkg in xml_pkgs)
        
        ## classes
        xml_class_root = ''
        if len(classes) > 0:
            xml_class_root = self.__make_sub('Classes', class_summary, False)
            xml_classes = []
            for cls in classes:
                xml_classes.append(self.__make_sub(cls.name, cls.uri, True))
            
            xml_class_root = xml_class_root % "\n".join(xml_class for xml_class in xml_classes)
        
        ## indexes
        xml_index_root = ''
        if len(indexes) > 0:
            xml_index_root = self.__make_sub('Indexes', index_list, False)
            xml_indexes = []
            for index in indexes:
                xml_indexes.append(self.__make_sub(index.name, index.uri, True))
            
            xml_index_root = xml_index_root % "\n".join(xml_index for xml_index in xml_indexes)
        
        ## extras
        xml_extra_root = ''
        if len(extras) > 0:
            xml_extra_root = self.__make_sub('Extras', '', False)
            xml_extras = []
            for extra in extras:
                xml_extras.append(self.__make_sub(extra.name, extra.uri, True))
            
            xml_extra_root = xml_extra_root % "\n".join(xml_extra for xml_extra in xml_extras)
        
        
        xml_chapters = "<chapters>\n%s\n</chapters>" % "\n".join(xml_chapter for xml_chapter in (xml_pkg_root, xml_class_root, xml_index_root, xml_extra_root))
        
        # Functions
        
        xml_functions = "<functions>\n%s\n</functions>" % ''
        
        # Book
        xml_book = '<book xmlns="%s" title="%s" name="%s" base="%s" link="%s" version="%d" language="%s">' % (Devhelp.XMLNS, self.title, self.name, root_path, index_link, Devhelp.VERSION, Devhelp.LANGUAGE)
        xml_book += "\n%s\n</book>" % "\n".join(xml_part for xml_part in (xml_chapters, xml_functions))
        
        xml = xml_header+xml_book
        return xml



