"""
The Member class encapsulates the interactions
with the UW Affiliation Group API resource
"""

import logging
import traceback
from django.conf import settings
from restclients.gws import GWS
from myuw_mobile.dao.pws import get_netid_of_current_user
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception


logger = logging.getLogger('myuw_mobile.dao.gws.Member')

def _is_member(groupid):
    """
    Return True if the current user netid is 
    an effective member of the given group
    """
    timer = Timer()
    try:
        return GWS().is_effective_member(groupid, 
                                         get_netid_of_current_user())
    except Exception as ex:
        log_exception(logger, 
                      'gws.is_effective_member of ' + groupid,
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      'gws.is_effective_member of ' + groupid,
                      timer)
    return None


def is_seattle_student():
    """
    Return True if the user is an UW Seattle student
    in the current quarter
    """
    return _is_member('uw_affiliation_seattle-student')


def is_bothell_student():
    """
    Return True if the user is an UW Bothell student
    in the current quarter
    """
    return _is_member('uw_affiliation_bothell-student')


def is_tacoma_student():
    """
    Return True if the user is an UW Tacoma student
    in the current quarter
    """
    return _is_member('uw_affiliation_tacoma-student')


def is_current_grad_student():
    """
    Return True if the user is an UW graduate student
    in the current quarter
    """
    return _is_member('uw_affiliation_graduate-current')

def is_grad_student():
    """
    Return True if the user is an UW graduate student 
    in the current, previous, or future quarter
    (Note by fl, 10/19/2012:
    If the student is a graduate and PCE student,
    uw affiliation group only reflects the first one.) 
    """
    return _is_member('uw_affiliation_graduate')


def is_undergrad_student():
    """
    Return True if the user is an UW undergraduate student 
    in the current, previous, or future quarter
    """
    return _is_member('uw_affiliation_undergraduate')


def is_pce_student():
    """
    Return True if the user is an UW PEC student 
    in the current, previous, or future quarter
    """
    return _is_member('uw_affiliation_extension-student')


def is_student_employee():
    """
    Return True if the user is an UW student employee (valid in 15 days) 
    """
    return _is_member('uw_affiliation_student-employee')

# The is_student function is in pws.py

