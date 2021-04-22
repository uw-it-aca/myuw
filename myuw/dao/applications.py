# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from uw_sdbmyuw import get_app_status
from myuw.dao import get_userids
from myuw.dao.pws import get_student_system_key_of_current_user

logger = logging.getLogger(__name__)


def get_applications(request):
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
