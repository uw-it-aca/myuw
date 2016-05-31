"""
This class encapsulates the interactions with
the SWS Personal Financial resource.
"""

import logging
from restclients.library.mylibinfo import get_account
from restclients.library.currics import get_subject_guide_for_section,\
    get_default_subject_guide
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
    get_default = False
    section_campus = section.course_campus.lower()
    try:
        subject_guide = get_subject_guide_for_section(section)
        if subject_guide.is_default_guide:
            default_campus = subject_guide.default_guide_campus.lower()
            if default_campus != section_campus:
                get_default = True
    except DataFailureException as ex:
        if ex.status == 404:
            get_default = True

    if get_default:
        subject_guide = get_default_subject_guide(section_campus)

    return subject_guide.guide_url
