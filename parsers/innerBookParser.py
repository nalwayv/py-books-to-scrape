"""
Parse a books link page using BeautifulSoup Tags 
to select wanted information 
"""
#--------------------------------------------------------------#
# IMPORTS

import re
import logging
from bs4.element import Tag as soupTag
from locators import bookPagesInfoLocators

#--------------------------------------------------------------#
# LOG

LOGGER = logging.getLogger("scrape.innerBookParser")

#--------------------------------------------------------------#
# CLASS


class InnerBookParser:
    """Users a BeautifulSoup Tag from the requests.get of BookParser link()"""

    def __init__(self, page: soupTag):
        LOGGER.debug("PARSING INFO ON MAIN BOOKS PAGE FOR STOCK AMOUNT")
        self.page = page

    def __repr__(self):
        return f"<{self.__class__.__name__}(), {self.stock}>"

    @property
    def stock(self):
        """Using css to locate the stock amount"""
        try:
            locator = bookPagesInfoLocators.STOCK

            find = self.page.select_one(locator).text

            stock = re.findall(r"\d+", find)

            return int(stock[0])

        except ValueError:
            raise ValueError("TRYED TO CONVERT STOCK TO INT AND FAILED")
            
#--------------------------------------------------------------#
