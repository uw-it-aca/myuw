"""
This class encapsulates the interactions with
the uwnetid subscription resource.
"""

import logging
import traceback
from restclients.uwnetid.subscription import get_email_forwarding
from restclients.exceptions import DataFailureException
from myuw_mobile.logger.logback import log_exception
from myuw_mobile.dao.pws import get_netid_of_current_user


logger = logging.getLogger(__name__)


def _get_email_forwarding_by_uwnetid(uwnetid):
    """
    returns restclients.models.uwnetid.UwEmailForwarding object
    for a given uwnetid
    """

    if uwnetid is None:
        return None

    id = "%s %s" % ('_get_email_forwarding_by_uwnetid', uwnetid)
    try:
        return get_email_forwarding(uwnetid)
    except Exception:
        log_exception(logger,
                      id,
                      traceback.format_exc())
    return None


def get_email_forwarding_for_current_user():
    return _get_email_forwarding_by_uwnetid(get_netid_of_current_user())
