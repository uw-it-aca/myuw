# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class encapsulates the interactions with
the UW attestion service.
"""
from restclients_core.exceptions import DataFailureException
from uw_attest import Attest
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao import is_using_file_dao, get_netid_of_current_user

Attestation = Attest()


def get_covid19_vaccination(request):
    """
    returns a list of uw_sws.models.StudentAdviser
    for the current user
    """
    if is_using_file_dao():
        if get_netid_of_current_user(request) == 'jerror':
            raise DataFailureException(
                "/attestations/v1/covid19", 500, "mock 500 error")
    return Attestation.get_covid19_vaccination(
        get_regid_of_current_user(request))
