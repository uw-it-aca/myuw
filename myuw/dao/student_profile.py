"""
This module encapsulates the interactions with the uw_sws.person,
provides student record information of the current user
"""

from uw_sws.person import get_person_by_regid
from myuw.dao.pws import get_regid_of_current_user


def get_profile_of_current_user():
    """
    Return uw_sws.models.SwsPerson object
    """
    regid = get_regid_of_current_user()
    return get_person_by_regid(regid)
