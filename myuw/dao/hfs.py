"""
This class encapsulates the interactions with
the student account balances (MyUW HFS) web service.
"""

import logging
from restclients.hfs.idcard import get_hfs_accounts
from restclients.exceptions import DataFailureException
from myuw.logger.logback import log_exception
from myuw.dao import get_netid_of_current_user


logger = logging.getLogger(__name__)


def get_account_balances_by_uwnetid(uwnetid):
    """
    returns restclients.models.hfs.HfsAccouts
    for the given uwnetid
    """
    if uwnetid is None:
        return None
    return get_hfs_accounts(uwnetid)


def get_account_balances_for_current_user():
    return get_account_balances_by_uwnetid(get_netid_of_current_user())
