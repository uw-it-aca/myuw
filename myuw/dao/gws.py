"""
The Member class encapsulates the interactions
with the UW Affiliation Group API resource
"""

import logging
from sets import Set, ImmutableSet
from django.conf import settings
from authz_group import Group
from uw_gws import GWS
from myuw.dao import get_netid_of_current_user, get_netid_of_original_user
from myuw.dao.pws import (is_bothell_employee, is_tacoma_employee,
                          is_seattle_employee, is_employee)
from myuw.dao.uwnetid import is_clinician, is_faculty


logger = logging.getLogger(__name__)
gws = GWS()

alumni = 'uw_affiliation_alumni'
alumni_asso = 'uw_affiliation_alumni-association-members'
applicant = 'uw_affiliation_applicant'
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
all_groups = [alumni, alumni_asso,
              applicant, staff, stud_emp,
              bot_stud, sea_stud, tac_stud,
              undergrad, grad, cur_grad_prof,
              pce, grad_c2, undergrad_c2]
RELEVANT_GROUPS = ImmutableSet(all_groups)


def _search_groups(uwnetid):
    """
    Returns a Set of the uw groups the uwnetid is an effective member of
    """
    group_names = Set([])
    group_refs = gws.search_groups(member=uwnetid,
                                   stem="uw_affiliation",
                                   scope="one",
                                   type="effective")
    if group_refs:
        for gr in group_refs:
            name = "%s" % gr.name
            if name in RELEVANT_GROUPS:
                group_names.add(name)
    return group_names


def get_groups(request):
    if not hasattr(request, "myuwgwsgroups"):
        request.myuwgwsgroups = _search_groups(
            get_netid_of_current_user(request))
    return request.myuwgwsgroups


def group_prefetch():
    def _method(request):
        return get_groups(request)
    return [_method]


def is_alumni(request):
    """
    In Advancement database (grace 30 days)
    """
    return alumni in get_groups(request)


def is_alum_asso(request):
    """
    A current alumni association member
    """
    return alumni_asso in get_groups(request)


def is_seattle_student(request):
    """
    An UW Seattle student in the current quarter
    """
    return sea_stud in get_groups(request)


def is_bothell_student(request):
    """
    An UW Bothell student in the current quarter
    """
    return bot_stud in get_groups(request)


def is_tacoma_student(request):
    """
    An UW Tacoma student in the current quarter
    """
    return tac_stud in get_groups(request)


def is_current_graduate_student(request):
    """
    In SDB, class is one of (00, 08, 11, 12, 13, 14),
    and status is Enrolled or on Leave
    """
    return cur_grad_prof in get_groups(request)


def is_grad_student(request):
    """
    A class-08 graduate student (grace 90 days),
    and status is not EO or applicant
    """
    return grad in get_groups(request)


def is_undergrad_student(request):
    """
    An UW undergraduate student class is one of (01, 02, 03, 04, 05, 06),
    (grace 90 days), and status is not EO or applicaNt
    """
    return undergrad in get_groups(request)


def is_student(request):
    return (is_undergrad_student(request) or
            is_current_graduate_student(request) or
            is_pce_student(request))


def is_pce_student(request):
    """
    An UW PEC student (grace 90 days)
    """
    return pce in get_groups(request)


def is_grad_c2(request):
    """
    An UW grad student taking PCE course (grace 90 days)
    """
    return grad_c2 in get_groups(request)


def is_undergrad_c2(request):
    """
    An undergrad student taking PCE cours (grace 90 days)
    """
    return undergrad_c2 in get_groups(request)


def is_student_employee(request):
    """
    An UW student employee (grace 15 days)
    """
    return stud_emp in get_groups(request)


def is_staff_employee(request):
    """
    An UW staff employee (grace 15 days)
    """
    return staff in get_groups(request)


def is_bothell_employee(request):
    return is_bothell_employee(request)


def is_seattle_employee(request):
    return is_seattle_employee(request)


def is_tacoma_employee(request):
    return is_tacoma_employee(request)


def is_applicant(request):
    """
    An UW applicant ((grace 90 days)
    """
    return applicant in get_groups(request)


def no_affiliation(request):
    return not is_employee(request) and\
        not is_student(request) and\
        not is_applicant(request) and\
        not is_clinician(request) and\
        not is_alumni(request)


def is_in_admin_group(group_key):
    if not hasattr(settings, group_key):
        print "You must have a group defined as your admin group."
        print 'Configure that using %s="foo_group"' % group_key
        raise Exception("Missing %s in settings" % group_key)

    actual_user = get_netid_of_original_user()
    if not actual_user:
        raise Exception("No user in session")

    group_name = getattr(settings, group_key)
    return Group().is_member_of_group(actual_user, group_name)
