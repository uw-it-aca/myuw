"""
This class encapsulates the interactions with
the SWS Personal Financial resource.
"""

import logging
import traceback
from restclients.library.mylibinfo import get_account
from restclients.exceptions import DataFailureException
from myuw_mobile.logger.logback import log_exception
from myuw_mobile.dao.pws import get_netid_of_current_user


logger = logging.getLogger(__name__)


def _get_account_by_uwnetid(uwnetid):
    """
    returns restclients.models.library.MyLibAccount object
    for a given uwnetid
    """

    if uwnetid is None:
        return None

    id = "%s %s" % ('_get_account_by_uwnetid', uwnetid)
    try:
        return get_account(uwnetid)
    except Exception:
        log_exception(logger,
                      id,
                      traceback.format_exc())
    return None


def get_account_info_for_current_user():
    return _get_account_by_uwnetid(get_netid_of_current_user())
