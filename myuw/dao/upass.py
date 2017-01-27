"""
This class encapsulates the interactions with
the UPass web service.
"""

import logging
from restclients.upass import get_upass_status
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time
from myuw.dao import get_netid_of_current_user


logger = logging.getLogger(__name__)


def get_upass_by_current_user():
    netid = get_netid_of_current_user()
    return get_upass_by_netid(netid)


def get_upass_by_netid(netid):
    """
    returns upass status for a netid
    """
    timer = Timer()
    try:
        return get_upass_status(netid)
    finally:
        log_resp_time(logger,
                      'get_upass_status',
                      timer)
