"""
This class encapsulates the interactions with the UPass web service.
"""

import logging
import re
from restclients.upass import get_upass_status
from myuw.dao import get_netid_of_current_user
from myuw.dao.gws import is_student, is_employee, is_student_employee


logger = logging.getLogger(__name__)


def get_upass_by_netid(netid):
    """
    returns upass status for a netid
    """
    status = get_upass_status(netid)
    status.is_employee = (status.is_employee or
                          (is_employee() and not is_student_employee()))
    status.is_student = (status.is_student or is_student())

    return status
