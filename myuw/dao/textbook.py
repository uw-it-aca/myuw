# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
encapsulates the interactions with the Bookstore web service.
"""

from uw_bookstore.digital_material import IACoursesStatus as Bookstore
from myuw.dao.pws import get_regid_of_current_user

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


def get_iacourse_status(request, term):
    """
    MUWM-5272
    returns a TermIACourse object if has data, otherwith return None
    """
    terms_iacourses = bookstore.get_iacourse_status(
        get_regid_of_current_user(request)
    )
    key = "{}{}".format(term.quarter, term.year)
    if key in terms_iacourses:
        return terms_iacourses.get(key)
    return None
