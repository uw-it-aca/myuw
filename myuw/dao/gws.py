"""
The Member class encapsulates the interactions
with the UW Affiliation Group API resource
"""

import logging
from restclients.gws import GWS
from myuw.dao import get_netid_of_current_user
from userservice.user import UserService
from django.conf import settings
from authz_group import Group


logger = logging.getLogger(__name__)


def _is_member(groupid):
    """
    Return True if the current user netid is
    an effective member of the given group
    """
    return GWS().is_effective_member(groupid,
                                     get_netid_of_current_user())


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


def is_graduate_student():
    """
    Return True if the user is an UW graduate student
    within 90 day, and status is not EO or applicaNt.
    """
    return _is_member('uw_affiliation_graduate')


def is_current_graduate_student():
    """
    Return True if the user is In SDB, class is one of
    (00, 08, 11, 12, 13, 14), and status is Enrolled or on Leave
    """
    return _is_member('uw_affiliation_graduate-current')


def is_grad_student():
    """
    Return True if the user is class-08 graduate student
    within 90 day, and status is not EO or applicaNt
    """
    return _is_member('uw_affiliation_graduate-grad')


def is_undergrad_student():
    """
    Return True if the user is an UW undergraduate student
    class is one of (01, 02, 03, 04, 05, 06),
    within 90 day, and status is not EO or applicaNt
    """
    return _is_member('uw_affiliation_undergraduate')


def is_student():
    return is_undergrad_student() or is_graduate_student()


def is_pce_student():
    """
    Return True if the user is an UW PEC student within 90 day
    """
    return _is_member('uw_affiliation_extension-student')


def is_student_employee():
    """
    Return True if the user is an UW student employee (valid in 15 days)
    """
    return _is_member('uw_affiliation_student-employee')


def is_faculty():
    """
    Return True if the user is UW faculty currently
    """
    return _is_member('uw_faculty')


# The is_student function is in pws.py


def is_employee():
    """
    Return True if the user is an UW employee currently
    """
    return _is_member('uw_employee')


def is_staff_employee():
    """
    Return True if the user is identified an UW staff employee
    within 15 days
    """
    return _is_member('uw_affiliation_staff-employee')


def is_applicant():
    """
    Return True if the user is identified a UW applicant
    """
    return _is_member('uw_affiliation_applicant')


def is_in_admin_group(group_key):
    user_service = UserService()
    user_service.get_user()
    override_error_username = None
    override_error_msg = None
    # Do the group auth here.

    if not hasattr(settings, group_key):
        print "You must have a group defined as your admin group."
        print 'Configure that using %s="foo_group"' % group_key
        raise Exception("Missing %s in settings" % group_key)

    actual_user = user_service.get_original_user()
    if not actual_user:
        raise Exception("No user in session")

    g = Group()
    group_name = getattr(settings, group_key)
    return g.is_member_of_group(actual_user, group_name)
