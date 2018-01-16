"""
The Member class encapsulates the interactions
with the UW Affiliation Group API resource
"""

import logging
from sets import Set, ImmutableSet
from uw_gws import GWS
from myuw.dao import get_netid_of_current_user, get_netid_of_original_user
from django.conf import settings
from authz_group import Group


logger = logging.getLogger(__name__)
gws = GWS()
applicant = 'uw_affiliation_applicant'
employee = 'uw_employee'
faculty = 'uw_faculty'
staff = 'uw_affiliation_staff-employee'
stud_emp = 'uw_affiliation_student-employee'
bot_stud = 'uw_affiliation_bothell-student'
sea_stud = 'uw_affiliation_seattle-student'
tac_stud = 'uw_affiliation_tacoma-student'
grad = 'uw_affiliation_graduate-grad'
cur_grad_prof = 'uw_affiliation_graduate-current'
undergrad = 'uw_affiliation_undergraduate'
pce = 'uw_affiliation_extension-student'
grad_c2 = 'uw_affiliation_continuum-student_graduate'
undergrad_c2 = 'uw_affiliation_continuum-student_undergraduate'

RELEVANT_GROUPS = ImmutableSet(
    [applicant, employee, faculty, staff, stud_emp,
     bot_stud, sea_stud, tac_stud, undergrad, grad,
     cur_grad_prof, pce, grad_c2, undergrad_c2])


def get_groups(uwnetid):
    """
    Returns a Set of the uw groups the uwnetid is an effective member of
    """
    group_names = Set([])
    group_refs = gws.search_groups(member=uwnetid,
                                   type="effective")
    if group_refs:
        for gr in group_refs:
            name = "%s" % gr.name
            if name in RELEVANT_GROUPS:
                group_names.add(name)
    return group_names


def groups_prefetch():
    def _method(request):
        return get_groups(get_netid_of_current_user())
    return [_method]


def is_seattle_student():
    """
    Return True if the user is an UW Seattle student
    in the current quarter
    """
    return sea_stud in get_groups(get_netid_of_current_user())


def is_bothell_student():
    """
    Return True if the user is an UW Bothell student
    in the current quarter
    """
    return bot_stud in get_groups(get_netid_of_current_user())


def is_tacoma_student():
    """
    Return True if the user is an UW Tacoma student
    in the current quarter
    """
    return tac_stud in get_groups(get_netid_of_current_user())


def is_current_graduate_student():
    """
    Return True if the user is In SDB, class is one of
    (00, 08, 11, 12, 13, 14), and status is Enrolled or on Leave
    """
    return cur_grad_prof in get_groups(get_netid_of_current_user())


def is_grad_student():
    """
    Return True if the user is class-08 graduate student
    within 90 day, and status is not EO or applicaNt
    """
    return grad in get_groups(get_netid_of_current_user())


def is_undergrad_student():
    """
    Return True if the user is an UW undergraduate student
    class is one of (01, 02, 03, 04, 05, 06),
    within 90 day, and status is not EO or applicaNt
    """
    return undergrad in get_groups(get_netid_of_current_user())


def is_student():
    return (is_undergrad_student() or
            is_current_graduate_student() or
            is_pce_student())


def is_pce_student():
    """
    Return True if the user is an UW PEC student within 90 day
    """
    return pce in get_groups(get_netid_of_current_user())


def is_grad_c2():
    """
    Return True if the grad student taking PCE course within 90 day
    """
    return _is_member('uw_affiliation_continuum-student_graduate')


def is_undergrad_c2():
    """
    Return True if the undergrad student taking PCE cours within 90 day
    """
    return _is_member('uw_affiliation_continuum-student_undergraduate')


def is_student_employee():
    """
    Return True if the user is an UW student employee (valid in 15 days)
    """
    return stud_emp in get_groups(get_netid_of_current_user())


def is_faculty():
    """
    Return True if the user is UW faculty currently
    """
    return faculty in get_groups(get_netid_of_current_user())


def is_employee():
    """
    Return True if the user is an UW employee currently
    """
    return employee in get_groups(get_netid_of_current_user())


def is_staff_employee():
    """
    Return True if the user is identified an UW staff employee
    within 15 days
    """
    return staff in get_groups(get_netid_of_current_user())


def is_applicant():
    """
    Return True if the user is identified a UW applicant
    """
    return applicant in get_groups(get_netid_of_current_user())


def is_in_admin_group(group_key):
    get_netid_of_current_user()
    override_error_username = None
    override_error_msg = None
    # Do the group auth here.

    if not hasattr(settings, group_key):
        print "You must have a group defined as your admin group."
        print 'Configure that using %s="foo_group"' % group_key
        raise Exception("Missing %s in settings" % group_key)

    actual_user = get_netid_of_original_user()
    if not actual_user:
        raise Exception("No user in session")

    group_name = getattr(settings, group_key)
    return gws.is_effective_member(group_name, actual_user)
