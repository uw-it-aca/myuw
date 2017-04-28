"""
The Member class encapsulates the interactions
with the UW Netid Web Service
"""

import logging
from restclients.uwnetid.subscription_60 import (is_current_faculty,
                                                 is_current_clinician)
from myuw.dao import get_netid_of_current_user
from restclients.exceptions import DataFailureException


logger = logging.getLogger(__name__)


def is_faculty():
    """
    Return True if the current user netid is
    a member of the UW Faculty
    """
    try:
        return is_current_faculty(get_netid_of_current_user())
    except DataFailureException as ex:
        if ex.status == 404:
            return False
        else:
            raise


def is_clinician():
    """
    Return True if the current user netid is
    a member of the UW Med Center Workforce
    """
    try:
        return is_current_clinician(get_netid_of_current_user())
    except DataFailureException as ex:
        if ex.status == 404:
            return False
        else:
            raise
