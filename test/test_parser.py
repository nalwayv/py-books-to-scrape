"""Testing to.scrape app for getting books from books.toscrape
"""
#-----------------------------------------------
# -- IMPORTS --

import sys
import os
sys.path.append(os.path.abspath(f"{__file__}/../.."))  # help with imports

# import unittest
import pytest
from bs4 import BeautifulSoup
from parsers import BookParser
from parsers import InnerBookParser

#-----------------------------------------------
# -- LOCATORS / HTML SAMPLES --

BOOK_LOCATOR = "li.col-xs-6"

STOCK = ".col-sm-6 p.instock"

# AN LI SAMPLE CONTAINING A SINGLE BOOKS WORTH OF DATA
BOOK_INFO_LI = """
<li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
    <article class="product_pod">
        <div class="image_container">
            <a href="a-light-in-the-attic_1000/index.html"><img src="../media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
                    alt="A Light in the Attic" class="thumbnail"></a>
        </div>
        <p class="star-rating Three">
            <i class="icon-star"></i>
            <i class="icon-star"></i>
            <i class="icon-star"></i>
            <i class="icon-star"></i>
            <i class="icon-star"></i>
        </p>
        <h3><a href="a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a></h3>

        <div class="product_price">

            <p class="price_color">£51.77</p>

            <p class="instock availability">
                <i class="icon-ok"></i>
                In stock
            </p>
            <form>
                <button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button>
            </form>
        </div>
    </article>
</li>
"""

# BOOK LI HAS A "LINK" TO A SEPERATE PAGE CONTAINING STOCK AMOUNT
BOOK_INFO_STOCK = """
<div class="col-sm-6 product_main">
    <h1>A Light in the Attic</h1>
    <p class="price_color">£51.77</p>
    <p class="instock availability">
        <i class="icon-ok"></i>
        In stock (22 available)
    </p>
    <p class="star-rating Three">
        <i class="icon-star"></i>
        <i class="icon-star"></i>
        <i class="icon-star"></i>
        <i class="icon-star"></i>
        <i class="icon-star"></i>
    </p>
    <hr>

    <div class="alert alert-warning" role="alert"><strong>Warning!</strong> This is a demo website for web scraping
        purposes. Prices and ratings here were randomly assigned and have no real meaning.</div>
</div>
"""

#-----------------------------------------------
# -- TESTING --


@pytest.mark.parametrize("title, stock, rating, price",
                         [("A Light in the Attic", 22, 3, 51.77)])
def test_parser(title, stock, rating, price):
    """Test parser's to get book info
    
    Parameters
    ----------
    title : str
        name of the book
    stock : int
        amount of books available
    rating : int
        score it was given
    price : float
        how much it costs
    
    """
    # main parser gets key info
    soup = BeautifulSoup(BOOK_INFO_LI, "html.parser")
    soup_page = soup.select_one(BOOK_LOCATOR)
    book = BookParser(soup_page)

    # stock is on another page
    # so main parser get a "link" that can be used to request another page
    soup_stock = BeautifulSoup(BOOK_INFO_STOCK, "html.parser")
    stock = InnerBookParser(soup_stock).stock
    book.stock = stock

    # test
    assert book.title == title
    assert book.stock == stock
    assert book.rating == rating
    assert book.price == price


#-----------------------------------------------
