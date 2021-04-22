# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class encapsulates the interactions with
the Grad School request resource.
"""

import logging
from datetime import date, datetime, timedelta
from uw_grad.degree import get_degree_by_syskey
from uw_grad.committee import get_committee_by_syskey
from uw_grad.leave import get_leave_by_syskey
from uw_grad.petition import get_petition_by_syskey
from myuw.dao.pws import get_student_system_key_of_current_user
from myuw.dao.term import get_comparison_datetime,\
    get_eod_specific_quarter_after, get_eod_specific_quarter,\
    get_eod_specific_quarter_last_instruction


logger = logging.getLogger(__name__)


def get_grad_degree_for_current_user(request):
    """
    returns json data of grad degree requests
    for the current user
    """
    return get_degree_by_syskey(
        get_student_system_key_of_current_user(request))


def get_grad_committee_for_current_user(request):
    """
    returns json data of grad degree requests
    for the current user
    """
    return get_committee_by_syskey(
        get_student_system_key_of_current_user(request))


def get_grad_leave_for_current_user(request):
    """
    returns json data of grad degree requests
    for the current user
    """
    return get_leave_by_syskey(
        get_student_system_key_of_current_user(request))


def get_grad_petition_for_current_user(request):
    """
    returns json data of grad degree requests
    for the current user
    """
    return get_petition_by_syskey(
        get_student_system_key_of_current_user(request))


def committee_to_json(req_data):
    """
    Simply convert the request object into JSON
    without filtering the data.
    """
    if req_data is None or len(req_data) == 0:
        return None
    result = []
    for item in req_data:
        result.append(item.json_data())
    return result


def degree_to_json(req_data, request):
    """
    Convert the degree request list object into JSON
    and remove the list item if it should not be shown.
    """
    if req_data is None or len(req_data) == 0:
        return None
    result = []
    now = get_comparison_datetime(request)

    for item in req_data:
        # Awaiting Dept Action,
        # Awaiting Dept Action (Final Exam),
        # Awaiting Dept Action (General Exam)
        # Recommended by Dept
        if item.is_status_await() or\
                item.is_status_recommended():
            # show during the status
            result.append(item.json_data())
            continue

        if item.is_status_graduated() or\
                item.is_status_candidacy() or\
                item.is_status_not_graduate():
            # show until eof the following quarter
            if now < get_eod_specific_quarter_after(item.target_award_year,
                                                    item.target_award_quarter):
                result.append(item.json_data())
            continue

        # For other statuses:
        if is_before_eof_2weeks_since_decision_date(item.decision_date, now):
            # show for 2 weeks after the decision date
            result.append(item.json_data())

    if len(result) == 0:
        return None
    return result


def is_before_eof_2weeks_since_decision_date(decision_date, now):
    """
    Return true if
    1). it is within the 2 week period after the decision date or
    2). no decision date is available.
    """
    return decision_date is None or\
        now < decision_date + timedelta(days=15)


def append_if_fn_apply(fn, result, item, now):
    """
    For each term in the leave request, append the json of the item
    if it's within the date obtained by applying the function given.
    """
    terms_json = []
    for gterm in item.terms:
        if now < fn(gterm.year, gterm.quarter):
            terms_json.append(gterm.json_data())

    if len(terms_json) > 0:
        req_json = item.json_data()
        req_json["terms"] = terms_json
        result.append(req_json)


def leave_to_json(req_data, request):
    """
    Convert the leave request list object into JSON
    and remove the list item if it should not be shown.
    """
    if req_data is None or len(req_data) == 0:
        return None
    result = []
    now = get_comparison_datetime(request)
    for item in req_data:
        if item.is_status_approved():
            # show until the end of the last instruction day of the leave term
            append_if_fn_apply(get_eod_specific_quarter_last_instruction,
                               result, item, now)
            continue

        if item.is_status_denied() or item.is_status_paid():
            # show until the end of the leave term
            append_if_fn_apply(get_eod_specific_quarter,
                               result, item, now)
            continue

        if item.is_status_requested():
            # show during the status
            result.append(item.json_data())
            continue

        if item.is_status_withdrawn():
            # show until eof the following quarter
            append_if_fn_apply(get_eod_specific_quarter_after,
                               result, item, now)
            continue

    if len(result) == 0:
        return None
    return result


def petition_to_json(req_data, request):
    """
    Convert the petition request list object into JSON
    and remove the list item if it should not be shown.
    """
    if req_data is None or len(req_data) == 0:
        return None
    result = []
    now = get_comparison_datetime(request)
    for item in req_data:
        if item.is_gs_pending():
            # in all three status of dept
            # show during the status
            result.append(item.json_data())
            continue

        # For other statuses:
        if is_before_eof_2weeks_since_decision_date(item.decision_date, now):
            # show for 2 weeks after the decision date
            result.append(item.json_data())

    if len(result) == 0:
        return None
    return result
