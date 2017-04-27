"""
encapsulates the interactions with the Bookstore web service.
"""

from restclients.bookstore import Bookstore


def get_textbook_by_schedule(schedule):
    """
    returns textbooks for a valid schedule
    """
    return Bookstore().get_books_for_schedule(schedule)


def get_verba_link_by_schedule(schedule):
    """
    returns a link to the verba price compare page for a valid schedule
    """
    return Bookstore().get_verba_link_for_schedule(schedule)
