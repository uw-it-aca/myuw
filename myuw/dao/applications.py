# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from restclients_core.exceptions import DataFailureException
from uw_sdbmyuw import get_app_status
from myuw.dao import get_userids, is_using_file_dao
from myuw.dao.pws import (
  get_netid_of_current_user, get_student_system_key_of_current_user)

logger = logging.getLogger(__name__)


def get_applications(request):
    if is_using_file_dao:
        netid = get_netid_of_current_user(request)
        if netid == 'jerror':
            raise DataFailureException(
                "/sdb_MyUW/appstatus.asp",
                500, "mock 500 error")

    response = []
    system_key = get_student_system_key_of_current_user(request)
    if system_key is not None:
        applications = get_app_status(system_key)
        for application in applications:
            response.append(application.json_data())
    else:
        logger.error({**get_userids(request),
                      **{'msg': "Missing Student System Key"}})
    return response
