"""
 ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
 ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
 ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
 ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
 ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
 ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝

SCRAPE DATA FROM BOOKS.TOSCRAPE.COM
"""
#--------------------------------------------------------------#
# -- IMPORTS --

import json
import logging
from pages import get_all_pages_books

#--------------------------------------------------------------#
# -- GLOBALS --

# create main singleton logger
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.DEBUG,
    filename="logs/logs.txt")

LOGGER = logging.getLogger("scraper")

JSON_FILE_NAME = "data/bookInfo.json"

#--------------------------------------------------------------#
# -- CUSTOM ERRORS --


class NoBooksFoundError(Exception):
    """Custom exception
    """

    def __init__(self, msg):
        super(NoBooksFoundError, self).__init__(msg)


#--------------------------------------------------------------#
# -- HELPERS  FUNCTIONS --


def write_to_json(data: dict):
    """write dict data to a json file
    
    Parameters
    ----------
    data : dict
        dict that contains an array of books
    
    """
    LOGGER.debug(f"WRITING BOOKS DATA TO {JSON_FILE_NAME}")

    file_name = JSON_FILE_NAME
    with open(file_name, "w") as j_file:
        json.dump(data, j_file, indent=4)


def get_books_from_json() -> list:
    """get books from json file

    Returns
    -------
    list
        list of dict books from json file books list
    """
    LOGGER.debug(f"LOADING BOOKS FROM {JSON_FILE_NAME}")

    file_name = JSON_FILE_NAME
    data = None
    with open(file_name, "r") as j_file:
        data = json.load(j_file)

    if data is None:
        raise NoBooksFoundError("NO BOOKS FOUND WITHIN DATABASE")

    return [book for book in data.get("books")]


def get_top_rated_books(books, amount: int) -> list:
    """Sort list by rating and return most reviewed
    
    Parameters
    ----------
    books : list
        list of book dict's
    amount : int
        slice list via amount to return
    
    Raises
    ------
    IndexError
        slice amount is bigger then the list
    
    Returns
    -------
    list
        list of books
    """
    if amount >= len(books) or amount < 0:
        raise IndexError("OUT OF RANGE")

    return sorted(books, key=lambda x: x.get("rating"), reverse=True)[:amount]


def get_cheepest_books(books, amount: int) -> list:
    """Sort list by stock and return cheepest
    
    Parameters
    ----------
    books : list
        list of book dict's
    amount : int
        slice list via amount to return
    
    Raises
    ------
    IndexError
        slice amount is bigger then the list
    
    Returns
    -------
    list
        list of books
    """
    if amount >= len(books) or amount < 0:
        raise IndexError("OUT OF RANGE")

    return sorted(books, key=lambda x: x.get("price"))[:amount]


def get_most_stocked_books(books, amount: int) -> list:
    """Sort list by stock and return most stocked
    
    Parameters
    ----------
    books : list
        list of book dict's
    amount : int
        slice list via amount to return
    
    Raises
    ------
    IndexError
        slice amount is bigger then the list
    
    Returns
    -------
    list
        list of sorted books by stock
    """

    if amount >= len(books) or amount < 0:
        raise IndexError("OUT OF RANGE")

    return sorted(books, key=lambda x: x.get("stock"), reverse=True)[:amount]


def scrape_books() -> list:
    """Scrape website to obtain books"""

    LOGGER.debug("STARTED SCRAPING NEW BOOK DATA")

    to_dict = lambda book:  dict(title=book.title, price=book.price, stock=book.stock, rating=book.rating)

    books = dict(books=[to_dict(book) for book in get_all_pages_books()])

    LOGGER.debug("FINISHED SCRAPING NEW BOOK DATA")

    write_to_json(books)

    return books.get("books")


#--------------------------------------------------------------#
# --INTERFACE FUNCTIONS --


def get_input(msg: str) -> str:
    """Get user input from console

    Parameters
    ----------
    msg : str
        message to display on what to enter

    Returns
    -------
    str
        string of what was entered
    """

    gi = ""
    while gi == "":
        gi = input(msg)
        if gi == "":
            print("ENTER SOMETHING PLEASE...")
    return gi


def get_choice(msg: str, arr: list) -> str:
    """Use when getting a user input from 
    a section of choices
    
    Parameters
    ----------
    msg : str
        message to display help
    arr : list
        list of choices that can be made
    
    Returns
    -------
    str
        string choice
    """
    print(f"{msg}")

    get_in = ""
    while get_in not in arr:
        get_in = get_input("> ").lower()

    return get_in


def quit_app() -> bool:
    """Quite the app

    Returns
    -------
    bool
        set whats running the main loop to false if set
    """
    gi = get_choice("ARE YOU SURE! Y[ES], N[O]", ["y", "n"])

    return False if gi == "y" else True


def print_info(books_list: list, msg: str):
    """Print information about books 
    
    Parameters
    ----------
    books_list : list
        list of dicts with key info
    msg : str
        message to be displayed about what is being shown
    
    """

    print(f"--- {msg} ---")

    print("-" * 20)

    for book in books_list:
        print(f"TITLE: {book.get('title','')}")
        print(f"PRICE: {book.get('price','')}")
        print(f"RATING: {book.get('rating','')}")
        print(f"STOCK: {book.get('stock','')}")
        print("-" * 20)


def switch(sym: str):
    """Return function based on symbol input
    
    Parameters
    ----------
    sym : str
        symbol used to get function
    
    Returns
    -------
    function
        function thatcan be invoked

    Example
    -------
        >> foo = switch("s")
        >> foo("foo")
    """

    try:
        return {
            "b": get_top_rated_books,
            "c": get_cheepest_books,
            "s": get_most_stocked_books
        }.get(sym, None)
    except TypeError:
        print("INVALID CHOICE")


def user_interface():
    """Main user interface"""

    LOGGER.debug("STARTING APP...")

    start_info = """
    SCRAPE BOOKS FROM BOOKS.TOSCRAPE.COM OR USED PRESCRAPED DATA
    !! -- SCAPING MIGHT TAKE A WHILE TO GET ALL WEBSITES BOOKS -- !!
    !! -- ALSO MIGHT FAIL DUE TO SITE NOT RESPONGING TO REQUEST -- !!
    S - SCRAPE 
    D - USE PRE-DATA
    """

    print(start_info)

    choice = get_choice("S[crape] or U[se json]", ["s", "u"])

    books = None
    if choice == "s":
        print("SCRAPING")
        books = scrape_books()
    else:
        print("USING JSON")
        books = get_books_from_json()

    info = f"""
    SCRAPED BOOKS FROM 'BOOKS.TOSCRAPE.COM'
    FOUND A TOTAL OF {len(books)} BOOKS...

    B - GET TOP TEN RATINGS
    C - GET TOP TEN CHEEPEST
    S - GET MOST STOCKED BOOKS
    Q - QUIT
    """

    # main loop
    running = True
    while running:
        print(info)

        usr_input: str = get_input("> ").lower()

        if usr_input == "q":
            running = quit_app()
        else:
            if usr_input in ["b", "c", "s"]:
                task = switch(usr_input)
                book_results = task(books, 10)
                print_info(book_results, "RESULT")

    print("EXITING...")
    LOGGER.debug("TERMINATING APP...")


def run():
    """Main app"""
    user_interface()


#--------------------------------------------------------------#
# -- MAIN --

if __name__ == "__main__":
    run()

#--------------------------------------------------------------#
