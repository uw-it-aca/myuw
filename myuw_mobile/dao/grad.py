"""
This class encapsulates the interactions with
the Grad School request resource.
"""

import logging
import traceback
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
        "degrees": json_data_degree(degree, request),
        "committees": json_data(committee),
        "leaves": json_data_leave(leave, request),
        "petitions": json_data_petition(petition, request)
        }


def json_data(req_data):
    """
    Simply convert the request object into JSON
    without any update of the data.
    """
    if req_data is None or len(req_data) == 0:
        return None
    result = []
    for item in req_data:
        result.append(item.json_data())
    return result


def json_data_degree(req_data, request):
    """
    Convert the degree request list object into JSON
    and remove the list item if it should not be shown.
    """
    if req_data is None or len(req_data) == 0:
        return None
    result = []
    for item in req_data:
        result.append(item.json_data())
    return result


def json_data_leave(req_data, request):
    """
    Convert the leave request list object into JSON
    and remove the list item if it should not be shown.
    """
    if req_data is None or len(req_data) == 0:
        return None
    result = []
    now = get_comparison_datetime(request)
    for item in req_data:
        # Approved: until eof last day of instruction
        if item.is_status_approved():
            append_if_fn_apply(get_eof_last_instruction_yq,
                               result, item, now)
            continue

        # Paid or Denied: until eof term
        if item.is_status_denied() or item.is_status_paid():
            append_if_fn_apply(get_eof_term_yq,
                               result, item, now)
            continue

        # Requested: Duration of status
        if item.is_status_requested():
            result.append(item.json_data())
            continue

        # Withdrawn: until eof the following quarter
        if item.is_status_withdrawn():
            append_if_fn_apply(get_eof_term_after_yq,
                               result, item, now)
            continue

    return result


def append_if_fn_apply(fn, result, item, now):
    terms_json = []
    for gterm in item.terms:
        if now < fn(gterm.year, gterm.quarter):
            terms_json.append(gterm.json_data())

    if len(terms_json) > 0:
        req_json = item.json_data()
        req_json["terms"] = terms_json
        result.append(req_json)


def json_data_petition(req_data, request):
    """
    Convert the petition request list object into JSON
    and remove the list item if it should not be shown.
    """
    if req_data is None or len(req_data) == 0:
        return None
    result = []
    for item in req_data:
        result.append(item.json_data())
    return result
