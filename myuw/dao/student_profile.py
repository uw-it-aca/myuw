"""
This module encapsulates the interactions with the restclients.sws.person,
provides student record information of the current user
"""

from restclients.sws.person import get_person_by_regid
from myuw.dao.pws import get_regid_of_current_user


def get_profile_of_current_user():
    """
    Return restclients.models.sws.SwsPerson object
    """
    regid = get_regid_of_current_user()
    return get_person_by_regid(regid)
