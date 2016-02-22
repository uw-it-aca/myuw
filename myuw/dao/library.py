"""
This class encapsulates the interactions with
the SWS Personal Financial resource.
"""

import logging
from restclients.library.mylibinfo import get_account
from restclients.digitlib.curric import get_subject_guide
from restclients.exceptions import DataFailureException
from myuw.logger.logback import log_exception
from myuw.dao.pws import get_netid_of_current_user


logger = logging.getLogger(__name__)


def _get_account_by_uwnetid(uwnetid):
    """
    returns restclients.models.library.MyLibAccount object
    for a given uwnetid
    """
    if uwnetid is None:
        return None
    return get_account(uwnetid)


def get_account_info_for_current_user():
    return _get_account_by_uwnetid(get_netid_of_current_user())


def get_subject_guide_by_section(section):
    """
    returns a url string
    """
    if section is None:
        return None
    return get_subject_guide(section.curriculum_abbr,
                             section.sln,
                             section.term.quarter,
                             section.term.year)
