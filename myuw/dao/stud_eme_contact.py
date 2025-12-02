# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from restclients_core.exceptions import DataFailureException
from uw_sps_contacts import EmergencyContacts
from myuw.dao import get_userids, is_using_file_dao
from myuw.dao.pws import (
  get_netid_of_current_user, get_student_system_key_of_current_user)


logger = logging.getLogger(__name__)
stud_eme_contact = EmergencyContacts()


def get_eme_contacts(request):
    if is_using_file_dao:
        netid = get_netid_of_current_user(request)
        if netid == 'jerror':
            raise DataFailureException(
                "contacts/v1/emergencyContacts/",
                500, "mock 500 error")

    json_values = []
    system_key = get_student_system_key_of_current_user(request)
    if system_key is not None:
        values = stud_eme_contact.get_contacts(
            get_student_system_key_of_current_user(request))

        for contact in values:
            json_values.append(contact.json_data())
    else:
        logger.error(
            {**get_userids(request),
             **{'msg': "Missing Student System Key"}})
    return json_values
