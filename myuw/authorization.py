# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
from uw_pws import PWS
from myuw.dao.admin import can_override, is_admin
from myuw.dao import pws

INVALID_STRING = "Username not a valid netid"
NO_USER = "No override user supplied, please enter a UWNetID"


def validate_netid(username):
    if len(username) == 0:
        return NO_USER

    if not PWS().valid_uwnetid(username) or len(username) > 64:
        # max for shared netid is 64
        return INVALID_STRING

    return None


def can_override_user(request):
    """
    Return True if the original user has impersonate permission
    """
    if not hasattr(request, "can_override_user"):
        request.can_override_user = can_override()
    return request.can_override_user


def can_proxy_restclient(request, service, url):
    """
    Return True if the original user has admin permission
    """
    if not hasattr(request, "can_proxy_restclient"):
        request.can_proxy_restclient = is_admin()
    return request.can_proxy_restclient


def is_myuw_admin(request):
    return can_proxy_restclient(request, "MyUW Support", "")
