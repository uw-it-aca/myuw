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
                                   scope="all",
                                   type="effective")
    if group_refs:
        for gr in group_refs:
            name = "%s" % gr.name
            if name in RELEVANT_GROUPS:
                group_names.add(name)
    return group_names


def get_groups(request):
    if hasattr(request, "myuwgwsgroups"):
        return request.myuwgwsgroups
    groups = _search_groups(get_netid_of_current_user(request))
    if groups:
        request.myuwgwsgroups = groups
        # we do not cache None value (rare case) in request
    return groups


def group_prefetch():
    def _method(request):
        return get_groups(request)
    return [_method]


def is_alumni(request):
    """
    In Advancement database (grace 30 days)
    """
    groups = get_groups(request)
    return groups is not None and alumni in groups


def is_alum_asso(request):
    """
    A current alumni association member
    """
    groups = get_groups(request)
    return groups is not None and alumni_asso in groups


def is_seattle_student(request):
    """
    An UW Seattle student in the current quarter
    """
    groups = get_groups(request)
    return groups is not None and sea_stud in groups


def is_bothell_student(request):
    """
    An UW Bothell student in the current quarter
    """
    groups = get_groups(request)
    return groups is not None and bot_stud in groups


def is_tacoma_student(request):
    """
    An UW Tacoma student in the current quarter
    """
    groups = get_groups(request)
    return groups is not None and tac_stud in groups


def is_current_graduate_student(request):
    """
    In SDB, class is one of (00, 08, 11, 12, 13, 14),
    and status is Enrolled or on Leave
    """
    groups = get_groups(request)
    return groups is not None and cur_grad_prof in groups


def is_grad_student(request):
    """
    A class-08 graduate student (grace 90 days),
    and status is not EO or applicant
    """
    groups = get_groups(request)
    return groups is not None and grad in groups


def is_undergrad_student(request):
    """
    An UW undergraduate student class is one of (01, 02, 03, 04, 05, 06),
    (grace 90 days), and status is not EO or applicaNt
    """
    groups = get_groups(request)
    return groups is not None and undergrad in groups


def is_student(request):
    return (is_undergrad_student(request) or
            is_current_graduate_student(request) or
            is_pce_student(request))


def is_pce_student(request):
    """
    An UW PEC student (grace 90 days)
    """
    groups = get_groups(request)
    return groups is not None and pce in groups


def is_grad_c2(request):
    """
    An UW grad student taking PCE course (grace 90 days)
    """
    groups = get_groups(request)
    return groups is not None and grad_c2 in groups


def is_undergrad_c2(request):
    """
    An undergrad student taking PCE cours (grace 90 days)
    """
    groups = get_groups(request)
    return groups is not None and undergrad_c2 in groups


def is_student_employee(request):
    """
    An UW student employee (grace 15 days)
    """
    groups = get_groups(request)
    return groups is not None and stud_emp in groups


def is_staff_employee(request):
    """
    An UW staff employee (grace 15 days)
    """
    groups = get_groups(request)
    return groups is not None and staff in groups


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
    groups = get_groups(request)
    return groups is not None and applicant in groups


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
