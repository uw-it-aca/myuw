# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class encapsulates the interactions with the UPass web service.
"""

from datetime import timedelta
from uw_admin_systems.upass import get_upass_status
from myuw.dao import get_netid_of_current_user
from myuw.dao.gws import is_student
from myuw.dao.term import (
    Term, get_comparison_datetime, get_current_quarter,
    get_bod_days_before_last_instruction)


def _get_upass_status(request):
    return get_upass_status(get_netid_of_current_user(request))


def get_upass(request):
    """
    returns upass status for a netid
    """
    status = _get_upass_status(request)
    ret_json = status.json_data()
    if is_student(request):
        ret_json['in_summer'] = in_summer_display_window(request)
    return ret_json


def in_summer_display_window(request):
    """
    Between the last day of class in spring quarter
    (the Friday before final week) to
    7 days before the 1st day of class in autumn quarter
    """
    now = get_comparison_datetime(request)
    cur_term = get_current_quarter(request)
    if cur_term.quarter.lower() == Term.SPRING:
        return now > get_bod_days_before_last_instruction(request, 1)
    if cur_term.is_summer_quarter():
        return True
    if cur_term.quarter.lower() == Term.AUTUMN:
        return now < (cur_term.get_bod_first_day() - timedelta(days=7))
