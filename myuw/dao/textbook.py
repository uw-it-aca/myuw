# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
encapsulates the interactions with the Bookstore web service.
"""

import logging
from uw_bookstore.digital_material import IACoursesStatus as Bookstore
from myuw.dao.pws import get_regid_of_current_user

bookstore = Bookstore()
logger = logging.getLogger(__name__)


def get_sln_textbook_json(quarter, sln_set):
    """
    returns a dict of sln to books in json format
    """
    sln_to_books = bookstore.get_textbook(quarter, sln_set)
    json_data = {}
    for sln in sln_set:
        json_data[sln] = []
        for book in sln_to_books.get(sln):
            json_data[sln].append(book.json_data())
    logger.debug(f"_get_textbook_json: {sln} {json_data[sln]}")
    return json_data


def get_order_url(quarter, sln_set):
    """
    returns a link to the bookstore ordering page for a given schedule
    """
    return bookstore.get_order_url(quarter, sln_set)


def get_iacourse_status(request, term):
    """
    MUWM-5272
    returns a TermIACourse object if has data, otherwith return None
    """
    terms_iacourses = bookstore.get_iacourse_status(
        get_regid_of_current_user(request)
    )
    key = "{}{}".format(term.quarter, term.year)
    return terms_iacourses.get(key)
