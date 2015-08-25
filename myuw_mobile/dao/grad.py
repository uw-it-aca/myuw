"""
This class encapsulates the interactions with
the Grad School request resource.
"""

import logging
import traceback
from datetime import date, datetime, timedelta
from restclients.grad.degree import get_degree_by_regid
from restclients.grad.committee import get_committee_by_regid
from restclients.grad.leave import get_leave_by_regid
from restclients.grad.petition import get_petition_by_regid
from myuw_mobile.logger.logback import log_exception
from myuw_mobile.dao.pws import get_regid_of_current_user
from myuw_mobile.dao.gws import is_grad_student
from myuw_mobile.dao.term import get_comparison_datetime
from myuw_mobile.dao.term.specific import get_eof_term_after_yq,\
    get_eof_term_yq, get_eof_last_instruction_yq


logger = logging.getLogger(__name__)


def get_grad_degree_for_current_user():
    """
    returns json data of grad degree requests
    for the current user
    """
    if not is_grad_student():
        return []  # not an error
    try:
        return get_degree_by_regid(get_regid_of_current_user())
    except Exception:
        log_exception(logger,
                      "get_grad_degree_for_current_user",
                      traceback.format_exc())
    return None


def get_grad_committee_for_current_user():
    """
    returns json data of grad degree requests
    for the current user
    """
    if not is_grad_student():
        return []  # not an error
    try:
        return get_committee_by_regid(get_regid_of_current_user())
    except Exception:
        log_exception(logger,
                      "get_grad_committee_for_current_user",
                      traceback.format_exc())
    return None


def get_grad_leave_for_current_user():
    """
    returns json data of grad degree requests
    for the current user
    """
    if not is_grad_student():
        return []  # not an error
    try:
        return get_leave_by_regid(get_regid_of_current_user())
    except Exception:
        log_exception(logger,
                      "get_grad_leave_for_current_user",
                      traceback.format_exc())
    return None


def get_grad_petition_for_current_user():
    """
    returns json data of grad degree requests
    for the current user
    """
    if not is_grad_student():
        return []  # not an error
    try:
        return get_petition_by_regid(get_regid_of_current_user())
    except Exception:
        log_exception(logger,
                      "get_grad_petition_for_current_user",
                      traceback.format_exc())
    return None


def get_json(degree, committee, leave, petition, request):
    return {
        "degrees": degree_to_json(degree, request),
        "committees": to_json(committee),
        "leaves": leave_to_json(leave, request),
        "petitions": petition_to_json(petition, request)
        }


def to_json(req_data):
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
            if now < get_eof_term_after_yq(item.target_award_year,
                                           item.target_award_quarter):
                result.append(item.json_data())
            continue

        # For other statuses:
        if is_before_eof_2weeks_since_decision_date(item.decision_date, now):
            # show for 2 weeks after the decision date
            result.append(item.json_data())
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
            append_if_fn_apply(get_eof_last_instruction_yq,
                               result, item, now)
            continue

        if item.is_status_denied() or item.is_status_paid():
            # show until the end of the leave term
            append_if_fn_apply(get_eof_term_yq,
                               result, item, now)
            continue

        if item.is_status_requested():
            # show during the status
            result.append(item.json_data())
            continue

        if item.is_status_withdrawn():
            # show until eof the following quarter
            append_if_fn_apply(get_eof_term_after_yq,
                               result, item, now)
            continue

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
    return result
