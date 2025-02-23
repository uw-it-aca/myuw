# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class interactes with the idcard eligibility web service.
"""

from uw_admin_systems.idcard import get_idcard_elig
from myuw.dao import get_netid_of_current_user


def get_idcard_eli(request):
    return get_idcard_elig(get_netid_of_current_user(request)).json_data()
