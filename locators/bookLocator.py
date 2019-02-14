"""Css Selectors for finding pages books"""
#--------------------------------------------------------------#
# -- IMPORTS --

from collections import namedtuple

#--------------------------------------------------------------#
# -- TUPLE DATA --

BOOKSLOCATOR = namedtuple("BooksLocator", ["BOOKS"])
BooksLocator = BOOKSLOCATOR(BOOKS="section ol.row li.col-xs-6")

#--------------------------------------------------------------#
