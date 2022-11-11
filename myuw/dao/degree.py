# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class encapsulates the interactions with
the student advisers.
"""
from restclients_core.exceptions import DataFailureException
from uw_sws.degree import get_degrees_by_regid
from myuw.dao import is_using_file_dao, get_netid_of_current_user
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.term import (
    four_wks_prior_last_day_inst,
    during_april_may, is_cur_term_before, is_cur_term_same)
from myuw.dao.term import more_than_2terms_before as before_display_window


def get_degrees(request):
    """
    returns a list of uw_sws.models.DegreeStatus
    for the current user
    """
    if is_using_file_dao():
        if get_netid_of_current_user(request) == 'jerror':
            raise DataFailureException(
                "/student/v5/person/degrees.json",
                500, "mock 500 error")
    return get_degrees_by_regid(get_regid_of_current_user(request))


def get_degrees_json(request):
    """
    MUWM-5009, MUWM-5010
    """
    response = {
        'degrees': None,
        'error_code': None
        }
    try:
        degrees = []
        for degree in get_degrees(request):
            if degree.is_granted():
                # Exclude if the degree earned term is older
                if before_display_window(request, degree.year, degree.quarter):
                    continue
            json_data = degree.json_data()
            during_april_may, is_cur_term_before, is_cur_term_same
            json_data["is_degree_earned_term"] = is_cur_term_same(
                request, degree.year, degree.quarter)
            json_data["before_degree_earned_term"] = is_cur_term_before(
                request, degree.year, degree.quarter)
            json_data["during_april_may"] = during_april_may(request)
            json_data["four_wks_prior_last_day_inst"] = \
                four_wks_prior_last_day_inst(request)
            degrees.append(json_data)
        response['degrees'] = degrees
    except DataFailureException as ex:
        response['error_code'] = ex.status
    return response
