# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
encapsulates the interactions with the Bookstore web service.
"""

from uw_bookstore import Bookstore


def get_textbook_by_schedule(schedule):
    """
    returns textbooks for a valid schedule
    """
    return Bookstore().get_books_for_schedule(schedule)


def get_order_url_by_schedule(schedule):
    """
    returns a link to the bookstore ordering page for a given schedule
    """
    return Bookstore().get_url_for_schedule(schedule)
