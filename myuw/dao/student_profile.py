"""
This module encapsulates the interactions with the uw_sws.person,
provides student record information of the current user
"""

from django.conf import settings
import logging
from uw_sws.person import get_person_by_regid
from myuw.dao.pws import get_regid_of_current_user
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time, log_exception, log_info

logger = logging.getLogger(__name__)


def get_profile_of_current_user():
    """
    Return uw_sws.models.SwsPerson object
    """
    regid = get_regid_of_current_user()

    timer = Timer()
    id = "%s %s" % ('get sws.person by regid', regid)
    try:
        return get_person_by_regid(regid)
    finally:
        log_resp_time(logger,
                      id,
                      timer)
