# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
dealing with the UW Affiliation Groups
"""

import logging
try:
    from sets import Set as set, ImmutableSet as frozenset
except ImportError:
    pass
from uw_gws import GWS
from myuw.util.settings import get_myuw_test_access_group
from myuw.dao import get_netid_of_current_user, get_netid_of_original_user
from myuw.dao.pws import is_employee


logger = logging.getLogger(__name__)
gws = GWS()

alumni_asso = 'uw_affiliation_alumni-association-members'
fhcrc_emp = 'uw_affiliation_fhcrc-employee'
medicine_aff = 'uw_affiliation_uw-medicine-affiliate'
medicine_wf = 'uw_affiliation_uw-medicine-workforce'
med_res = 'uw_affiliation_wwami-medical-resident'
medicine_staff = 'uw_affiliation_uwnc-staff'
scca_emp = 'uw_affiliation_scca-employee'
uwp_pro = 'uw_affiliation_uwp-provider'
uwp_staff = 'uw_affiliation_uwp-staff'
uwnc_staff = 'uw_affiliation_uwnc-staff'
applicant = 'uw_affiliation_applicant'
staff = 'uw_affiliation_staff-employee'
stud_emp = 'uw_affiliation_student-employee'
bot_stud = 'uw_affiliation_bothell-student'
sea_stud = 'uw_affiliation_seattle-student'
tac_stud = 'uw_affiliation_tacoma-student'
grad = 'uw_affiliation_graduate-grad'
undergrad = 'uw_affiliation_undergraduate'  # grace 90 days
grad_prof = 'uw_affiliation_graduate'  # grace 90 days
pce = 'uw_affiliation_extension-student'
grad_c2 = 'uw_affiliation_continuum-student_graduate'
undergrad_c2 = 'uw_affiliation_continuum-student_undergraduate'
all_groups = [alumni_asso, staff, medicine_wf, medicine_aff, medicine_staff,
              uwp_pro, uwp_staff, med_res, fhcrc_emp, scca_emp, uwnc_staff,
              applicant, stud_emp, bot_stud, sea_stud, tac_stud, undergrad,
              grad_prof, grad, pce, grad_c2, undergrad_c2]
RELEVANT_GROUPS = frozenset(all_groups)


def _search_groups(uwnetid):
    """
    Returns a Set of the uw groups the uwnetid is an effective member of
    """
    group_names = set([])
    group_refs = gws.search_groups(member=uwnetid,
                                   scope="all",
                                   type="direct",
                                   stem="uw_affiliation",
                                   name="")
    if group_refs:
        for gr in group_refs:
            name = str(gr.name)
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


def is_alum_asso(request):
    """
    A current alumni association member
    """
    return alumni_asso in get_groups(request)


def is_clinician(request):
    """
    As UW Medicine Workforce
    """
    return (medicine_aff in get_groups(request) or
            medicine_wf in get_groups(request) or
            medicine_staff in get_groups(request) or
            fhcrc_emp in get_groups(request) or
            scca_emp in get_groups(request) or
            uwp_pro in get_groups(request) or
            uwp_staff in get_groups(request) or
            uwnc_staff in get_groups(request) or
            med_res in get_groups(request))


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


def is_grad_and_prof_student(request):
    """
    In SDB, class is one of (00, 08, 11, 12, 13, 14),
    and status is Enrolled or on Leave, 90 days of grace status
    """
    return grad_prof in get_groups(request)


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
            is_grad_and_prof_student(request) or
            is_grad_student(request) or
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


def is_regular_employee(request):
    return ((is_employee(request) or is_clinician(request)) and
            not is_student_employee(request))


def is_applicant(request):
    """
    An UW applicant ((grace 90 days)
    """
    return applicant in get_groups(request)


def no_major_affiliations(request):
    return (not is_applicant(request) and
            not is_regular_employee(request) and
            not is_student(request))


def is_effective_member(request, group_id):
    return gws.is_effective_member(group_id,
                                   get_netid_of_current_user(request))


def in_myuw_test_access_group(request):
    test_access_group = get_myuw_test_access_group()
    return (test_access_group is None or
            gws.is_effective_member(get_myuw_test_access_group(),
                                    get_netid_of_original_user(request)))


def in_fyp_group(request):
    if not hasattr(request, "in_fyp_group"):
        request.in_fyp_group = is_effective_member(request, "u_myuwgroup_fyp")
    return request.in_fyp_group


def in_au_xfer_group(request):
    if not hasattr(request, "in_au_xfer_group"):
        request.in_au_xfer_group = is_effective_member(
            request, "u_myuwgroup_auxfer")
    return request.in_au_xfer_group


def in_wi_xfer_group(request):
    if not hasattr(request, "in_wi_xfer_group"):
        request.in_wi_xfer_group = is_effective_member(
            request, "u_myuwgroup_wixfer")
    return request.in_wi_xfer_group


def in_hxtoolkit_group(request):
    if not hasattr(request, "in_hxtoolkit_group"):
        request.in_hxtoolkit_group = is_effective_member(
            request, "u_myuwgroup_hxtoolkit")
    return request.in_hxtoolkit_group
