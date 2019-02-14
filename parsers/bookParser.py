"""
Parse a book using BeautifulSoup Tags to select wanted information
to then be returned
"""

#--------------------------------------------------------------#
# IMPORTS

import re
import logging
from bs4.element import Tag as soupTag
from locators import BookInfoLocators

#--------------------------------------------------------------#
# LOG

LOGGER = logging.getLogger("scrape.bookParser")

#--------------------------------------------------------------#
# CLASS


class BookParser:
    """Beautiful soup a books information"""

    def __init__(self, page: soupTag):
        LOGGER.debug("PARSING BOOKS <LI> INFO FOR TITLE,LINK,PRICE.")

        self.page: soupTag = page
        self.__stock = 0

    def __repr__(self):
        return f"<{self.__class__.__name__}(), TITLE: {self.title}, PRICE: {self.price}, LINK: {self.link} ,RATING: {self.rating}>"

    def __str__(self):
        return f"(TITLE: {self.title}, PRICE: {self.price}, LINK: {self.link} ,RATING: {self.rating})"

    @property
    def title(self) -> str:
        """Get books title
       
        Returns
        -------
        str
            name of the book
        """
        locator = BookInfoLocators.ATTR

        return self.page.select_one(locator).attrs.get("title", "")

    @property
    def link(self):
        """Get link to page that contains book information
        
        Returns
        -------
        str
            link to web page
        """
        locator = BookInfoLocators.ATTR

        url = self.page.select_one(locator).attrs.get("href", "")

        return f"http://books.toscrape.com/catalogue/{url}"

    @property
    def stock(self) -> int:
        """Get stock that is obtained from innerBookParser
        """
        return self.__stock

    @stock.setter
    def stock(self, value):
        self.__stock = value

    @property
    def price(self) -> float:
        """Get books price
       
        Returns
        -------
        float
            price of the book
        """

        try:
            locator = BookInfoLocators.PRICE
            find = self.page.select_one(locator).text

            # get the money
            match = re.search(r"£([0-9]+\.[0-9]+)", find)

            # match returns [£100 , 100]
            return float(match.group(1))
        except ValueError:
            raise ValueError("TRYED TO CONVERT PRICE TO FLOAT AND FAILED")

    @property
    def rating(self) -> int:
        """Get books rating
        
        Returns
        -------
        int
            score its recived
        """

        locator = BookInfoLocators.RATING

        find = [
            rating
            for rating in self.page.select_one(locator).attrs.get("class", "")
            if rating != "star-rating"
        ]

        # convert word score to num score
        return {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5
        }.get(find[0].lower(), -1)


#--------------------------------------------------------------#
