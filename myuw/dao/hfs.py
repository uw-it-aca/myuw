# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class encapsulates the interactions with
the student account balances (MyUW HFS) web service.
"""

import logging
from uw_hfs.idcard import get_hfs_accounts
from restclients_core.exceptions import DataFailureException
from myuw.dao import get_netid_of_current_user


logger = logging.getLogger(__name__)


def get_account_balances_by_uwnetid(uwnetid):
    """
    returns uw_hfs.models.HfsAccouts
    for the given uwnetid
    """
    if uwnetid is None:
        return None
    return get_hfs_accounts(uwnetid)


def get_account_balances_for_current_user(request):
    return get_account_balances_by_uwnetid(get_netid_of_current_user(request))
