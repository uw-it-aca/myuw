# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class encapsulates the interactions with
the uwnetid subscription resource.
"""

import logging
from uw_uwnetid.password import get_uwnetid_password
from myuw.dao.term import get_comparison_datetime_with_tz
from myuw.dao import get_netid_of_current_user


logger = logging.getLogger(__name__)


def get_password_info(request):
    """
    returns uw_netid.models.UwPassword object
    for a given uwnetid
    """
    if not hasattr(request, "myuw_netid_password"):
        request.myuw_netid_password = get_uwnetid_password(
            get_netid_of_current_user(request))
    return request.myuw_netid_password


def password_prefetch():
    def _method(request):
        get_password_info(request)
    return [_method]


def get_pw_json(request):
    """
    return data attributes:
    {
    "uwnetid":
    "kerb_status": string
    "last_change": date
    "interval": seconds or null
    "last_change_med": date
    "expires_med": date
    "interval_med": seconds
    "minimum_length": integer
    "time_stamp": date
    "netid_status": list of strings
    }
    """
    pw = get_password_info(request)
    return pw.json_data() if pw else None
