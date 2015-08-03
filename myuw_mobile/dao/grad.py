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


logger = logging.getLogger(__name__)


def get_grad_degree_for_current_user():
    """
    returns json data of grad degree requests
    for the current user
    """

    try:
        if is_grad_student():
            return get_degree_by_regid(get_regid_of_current_user())
        return []  # not an error
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

    try:
        if is_grad_student():
            return get_committee_by_regid(get_regid_of_current_user())
        return []  # not an error
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

    try:
        if is_grad_student():
            return get_leave_by_regid(get_regid_of_current_user())
        return []  # not an error
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

    try:
        if is_grad_student():
            return get_petition_by_regid(get_regid_of_current_user())
        return []  # not an error
    except Exception:
        log_exception(logger,
                      "get_grad_petition_for_current_user",
                      traceback.format_exc())
    return None


def get_json(degree, committee, leave, petition):
    return {
        "degrees": json_data(degree),
        "committees": json_data(committee),
        "leaves": json_data(leave),
        "petitions": json_data(petition)
        }


def json_data(req_data):
    if req_data is None or len(req_data) == 0:
        return None
    result = []
    for item in req_data:
        result.append(item.json_data())
    return result
