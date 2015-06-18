"""
This module encapsulates the interactions with the restclients.sws.person,
provides student record information of the current user
"""

from django.conf import settings
import logging
import traceback
from restclients.sws.person import get_person_by_regid
from myuw_mobile.dao.pws import get_regid_of_current_user
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception, log_info

logger = logging.getLogger(__name__)


def get_profile_of_current_user():
    """
    Return restclients.models.sws.SwsPerson object
    """
    regid = get_regid_of_current_user()

    timer = Timer()
    id = "%s %s" % ('get sws.person by regid', regid)
    try:
        return get_person_by_regid(regid)
    except Exception:
        log_exception(logger,
                      id,
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      id,
                      timer)
    return None
