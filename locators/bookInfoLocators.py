"""
Css Selectors for finding book information
"""

#--------------------------------------------------------------#
# -- IMPORTS --

from collections import namedtuple

#--------------------------------------------------------------#
# -- TUPLE DATA --

BOOKINFO = namedtuple("BookInfo", ["ATTR", "PRICE", "RATING"])

BookInfoLocators = BOOKINFO(
    ATTR="article.product_pod h3 a",
    PRICE="article.product_pod .product_price p.price_color",
    RATING="article.product_pod p.star-rating")

#--------------------------------------------------------------#
