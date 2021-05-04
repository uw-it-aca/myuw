# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class encapsulates the interactions with
the student advisers.
"""
from restclients_core.exceptions import DataFailureException
from uw_sws.adviser import get_advisers_by_regid
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao import is_using_file_dao, get_netid_of_current_user


def get_academic_advisers(request):
    """
    returns a list of uw_sws.models.StudentAdviser
    for the current user
    """
    if is_using_file_dao():
        if get_netid_of_current_user(request) == 'jerror':
            raise DataFailureException(
                "/student/v5/person/advisers.json",
                500, "mock 500 error")
    return get_advisers_by_regid(get_regid_of_current_user(request))
