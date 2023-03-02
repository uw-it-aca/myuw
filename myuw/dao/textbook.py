# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
encapsulates the interactions with the Bookstore web service.
"""

from uw_bookstore import Bookstore

bookstore = Bookstore()


def get_textbook_by_schedule(schedule):
    """
    returns textbooks for a valid schedule
    """
    return bookstore.get_books_for_schedule(schedule)


def get_order_url_by_schedule(schedule):
    """
    returns a link to the bookstore ordering page for a given schedule
    """
    return bookstore.get_url_for_schedule(schedule)
