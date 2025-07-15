# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
encapsulates the interactions with the Bookstore web service.
"""

import logging
from restclients_core.exceptions import DataFailureException
from uw_bookstore import Textbook
from uw_bookstore.digital_material import IACoursesStatus as Bookstore
from myuw.dao.pws import get_regid_of_current_user

bookstore = Bookstore()
logger = logging.getLogger(__name__)


def get_textbook_json(quarter, sln_set):
    """
    returns a dict in json format
    """
    result = bookstore.get_textbooks(quarter, sln_set)
    if result is None:
        return {}
    json_data = {"order_url": None}
    course_ids = []
    search_url = None
    for sln in sln_set:
        json_data[sln] = {}
        value = result.get(sln)
        if isinstance(value, Textbook):
            json_data[sln] = value.json_data()
            course_ids.append(value.course_id)
            if not search_url:
                search_url = value.search_url
            continue
        if isinstance(value, DataFailureException):
            json_data[sln]["error"] = str(value)
    json_data["order_url"] = get_search_url(search_url, course_ids)
    logger.debug(f"get_textbook_json {quarter} {sln_set} ==> {json_data}")
    return json_data


def get_search_url(search_url, course_ids):
    if search_url and course_ids:
        query_str = ','.join(sorted(course_ids))
        return f"{search_url}{query_str}"
    return search_url


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
