"""
This class encapsulates the interactions with 
the SWS Personal Financial resource.
"""

import logging
import traceback
from restclients.sws.financial import get_account_balances_by_regid
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception, log_info
from myuw_mobile.dao.pws import get_regid_of_current_user

logger = logging.getLogger(__name__)

def _get_account_balances_by_regid(user_regid):
    """
    returns restclients.models.sws.Finance object for a given regid
    """

    if user_regid is None:
        return None

    timer = Timer()
    id = "%s %s" % ('_get_account_balances_by_regid', user_regid) 
    try:
        return get_account_balances_by_regid(user_regid)
    except Exception:
        log_exception(logger,
                      id,
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      id,
                      timer)
    return None


def get_account_balances_for_current_user():
    return _get_account_balances_by_regid(get_regid_of_current_user())
