"""
This module encapsulates the interactions with the restclients.pws,
provides information of the current user
"""

from django.conf import settings
import logging
import traceback
from restclients.pws import PWS
from userservice.user import UserService
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time, log_exception, log_info
import re

logger = logging.getLogger(__name__)


def get_netid_of_current_user():
    username = UserService().get_user()

    username = descope_uw_username(username)
    return username


def descope_uw_username(username):
    if re.match(r'.*@washington.edu$', username):
        return username.replace('@washington.edu', '')
    return username


def _get_person_of_current_user():
    """
    Retrieve the person data using the netid of the current user
    """
    timer = Timer()
    try:
        return PWS().get_person_by_netid(get_netid_of_current_user())
    except Exception as ex:
        log_exception(logger,
                      'pws.get_person_by_netid',
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      'pws.get_person_by_netid',
                      timer)
    return None


def get_regid_of_current_user():
    """
    Return the regid of the current user
    """
    res = _get_person_of_current_user()
    if res is not None:
        return res.uwregid


def is_student():
    """
    Return true if the user is an
    UW undergraduate/graduate/onleave graduate/pce students
    who are enrolled for the current quarter,
    the previous quarter, or a future quarter
    """
    res = _get_person_of_current_user()
    if res is not None:
        return res.is_student
