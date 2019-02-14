"""
Using requests / BeautifulSoup soup and BookParser to scrape data from a single page
or multiple pages 
"""

#--------------------------------------------------------------#
# -- IMPORTS --

import logging
import requests
from bs4 import BeautifulSoup
from locators import BooksLocator
from parsers import BookParser
from parsers import InnerBookParser

#--------------------------------------------------------------#
# -- LOG --

LOGGER = logging.getLogger("scraper.book_pages")

#--------------------------------------------------------------#
# -- FUNCTIONS --


def get_pages_books(page) -> list:
    """Return a list of books on a single page

    Parameters
    ----------
    page : requests.Responce.content
        content obtained from a requests.get() call to a web url

    Returns
    -------
    list
        list of BookParse obj's
    """
    LOGGER.debug(f"GETTING BOOKS FROM PAGE {page.url}")

    soup = BeautifulSoup(page.content, "html.parser")
    locator = BooksLocator.BOOKS

    res = []
    for book in soup.select(locator):
        new_book = BookParser(book)
        new_book.stock = get_books_stock(new_book.link)
        res.append(new_book)
    return res


def get_books_stock(link: str) -> int:
    """Use the InnerBookParser class with requsts to get stock amount
    from books link obtained from BookParser

    Parameters
    ----------
    link : str
        string format of the url link
    Returns
    -------
    int
        amount of stock 
    """
    page = requests.get(link)

    if page.status_code == 404:
        return -1

    soup = BeautifulSoup(page.content, "html.parser")
    return InnerBookParser(soup).stock


# PUBLIC
def get_all_pages_books(idx: int = 1) -> list:
    """With recursion go over each page on book.toscrape and retrive books using get_pages_books 
    until a 404 status code is made stopping the loop
    
    Parameters
    ----------
    idx : int, optional
        number of the page (the default is 1, which the first page)
    
    Returns
    -------
    list
        list of BookParse objs
    """
    # get web page
    LOGGER.info("SCRAPING BOOKS FROM 'BOOKS.TOSCRAPE.COM'")

    page = requests.get(f"http://books.toscrape.com/catalogue/page-{idx}.html")

    # stop once a 404 error has been made
    # return an empty array that all books will be appended to
    if page.status_code == 404:
        return []

    # go to next page plus append current pages books to list
    # concat arrays array + another array
    return get_all_pages_books(idx + 1) + get_pages_books(page)
