"""
This module encapsulates the interactions with the restclients.pws,
provides information of the current user
"""

import logging
from restclients.pws import PWS
from myuw.dao import get_netid_of_current_user


logger = logging.getLogger(__name__)


def get_person_of_current_user():
    """
    Retrieve the person data using the netid of the current user
    """
    return PWS().get_person_by_netid(get_netid_of_current_user())


def get_regid_of_current_user():
    """
    Return the regid of the current user
    """
    res = get_person_of_current_user()
    return res.uwregid


def get_display_name_of_current_user():
    """
    Return the display_name of the current user
    """
    res = get_person_of_current_user()
    return res.display_name


def is_student():
    """
    Return true if the user is an
    UW undergraduate/graduate/onleave graduate/pce students
    who are enrolled for the current quarter,
    the previous quarter, or a future quarter
    """
    res = get_person_of_current_user()
    return res.is_student


def person_prefetch():
    def _method(request):
        return get_person_of_current_user()

    return [_method]


def get_url_key_for_regid(regid):
    # XXX - I want a hook to obscure/encrypt this down the road
    return regid


def get_regid_for_url_key(key):
    return key


def get_idcard_photo(regid):
    return PWS().get_idcard_photo(regid)
    pass
