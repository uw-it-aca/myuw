"""
This module encapsulates the interactions with the restclients.pws,
provides information of the current user
"""

import logging
from django.conf import settings
from restclients.pws import PWS
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time, log_exception, log_info
from myuw.dao import get_netid_of_current_user


logger = logging.getLogger(__name__)


def _get_person_of_current_user():
    """
    Retrieve the person data using the netid of the current user
    """
    timer = Timer()
    try:
        return PWS().get_person_by_netid(get_netid_of_current_user())
    finally:
        log_resp_time(logger,
                      'pws.get_person_by_netid',
                      timer)


def get_regid_of_current_user():
    """
    Return the regid of the current user
    """
    res = _get_person_of_current_user()
    return res.uwregid


def get_display_name_of_current_user():
    """
    Return the display_name of the current user
    """
    res = _get_person_of_current_user()
    return res.display_name


def is_student():
    """
    Return true if the user is an
    UW undergraduate/graduate/onleave graduate/pce students
    who are enrolled for the current quarter,
    the previous quarter, or a future quarter
    """
    res = _get_person_of_current_user()
    return res.is_student
