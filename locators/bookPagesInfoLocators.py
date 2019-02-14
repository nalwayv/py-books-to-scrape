"""
Css Locator for finding stock tag
"""
#--------------------------------------------------------------#
# -- IMPORTS --

from collections import namedtuple

#--------------------------------------------------------------#
# -- TUPLE DATA --

BOOKPAGESINFOLOCATORS = namedtuple("bookPagesInfoLocators", ["STOCK"])
bookPagesInfoLocators = BOOKPAGESINFOLOCATORS(STOCK=".col-sm-6 p.instock")

#--------------------------------------------------------------#
