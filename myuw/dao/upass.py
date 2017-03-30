"""
This class encapsulates the interactions with the UPass web service.
"""

from datetime import timedelta
import logging
import re
from restclients.upass import get_upass_status
from myuw.dao import get_netid_of_current_user
from myuw.dao.term import Term, get_comparison_datetime,\
    get_current_quarter, get_next_quarter
from myuw.dao.gws import is_student, is_employee, is_student_employee


logger = logging.getLogger(__name__)


def upass_prefetch():

    def _method(request):
        get_upass_status(get_netid_of_current_user())

    return [_method]


def get_upass_by_netid(netid, request):
    """
    returns upass status for a netid
    """
    status = get_upass_status(netid)
    ret_json = status.json_data()

    if status.is_current:
        ret_json['display_activation'] = (status.is_employee or
                                          around_qtr_begin(request))
    ret_json['is_employee'] = (status.is_employee or
                               (is_employee() and not is_student_employee()))
    ret_json['is_student'] = (status.is_student or is_student())

    if ret_json['is_student']:
        ret_json['in_summer'] = in_summer_display_window(request)

    return ret_json


def around_qtr_begin(request):
    """
    Between 7 days before the 1st day of class to 14 days after it
    """
    now = get_comparison_datetime(request)
    term = get_current_quarter(request)
    if now > term.get_eod_last_instruction():
        term = get_next_quarter(request)
    start = term.get_bod_first_day() - timedelta(days=7)
    end = term.get_bod_first_day() + timedelta(days=15)
    return (now > start and now < end)


def in_summer_display_window(request):
    """
    Between the last day of class in spring quarter
    (the Friday before final week) to
    7 days before the 1st day of class in autumn quarter
    """
    now = get_comparison_datetime(request)
    cur_term = get_current_quarter(request)
    if cur_term.quarter.lower() == Term.SPRING:
        return now > (cur_term.get_eod_last_instruction() - timedelta(days=1))
    if cur_term.is_summer_quarter():
        return True
    if cur_term.quarter.lower() == Term.AUTUMN:
        return now < (cur_term.get_bod_first_day() - timedelta(days=7))
