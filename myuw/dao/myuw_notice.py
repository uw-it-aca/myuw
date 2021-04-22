# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from myuw.dao.affiliation import get_all_affiliations
from myuw.models.myuw_notice import MyuwNotice
from myuw.dao.gws import is_effective_member
from myuw.dao.term import get_comparison_datetime_with_tz


def get_myuw_notices_for_user(request):
    date = get_comparison_datetime_with_tz(request)
    fetched_notices = MyuwNotice.objects.filter(start__lte=date)
    affiliations = get_all_affiliations(request)

    user_notices = []
    for notice in fetched_notices:

        if notice.end is not None and notice.end < date:
            # exclude those past display time window
            continue

        if notice.has_target_group():
            if is_effective_member(request, notice.target_group):
                user_notices.append(notice)
            continue

        if for_all_affi(notice):
            if (is_stud_campus_matched(notice, affiliations) or
                    is_employee_campus_matched(notice, affiliations)):
                user_notices.append(notice)
            continue

        if student_affiliation_matched(notice, affiliations):
            if is_stud_campus_matched(notice, affiliations):
                user_notices.append(notice)
            continue

        if employee_affiliation_matched(notice, affiliations):
            if is_employee_campus_matched(notice, affiliations):
                user_notices.append(notice)
            continue

    return user_notices


def campus_neutral(notice):
    return not (notice.is_bothell or notice.is_seattle or notice.is_tacoma)


def is_stud_campus_matched(notice, affiliations):
    return (campus_neutral(notice) or
            notice.is_seattle and affiliations['seattle'] or
            notice.is_bothell and affiliations['bothell'] or
            notice.is_tacoma and affiliations['tacoma'])


def is_employee_campus_matched(notice, affiliations):
    return (campus_neutral(notice) or
            notice.is_seattle and affiliations['official_seattle'] or
            notice.is_bothell and affiliations['official_bothell'] or
            notice.is_tacoma and affiliations['official_tacoma'])


def for_all_affi(notice):
    """
    no affiliation is selected
    """
    return not (notice.is_alumni or notice.is_applicant or
                notice.is_grad or notice.is_grad_c2 or
                notice.is_pce or notice.is_student or
                notice.is_undergrad or notice.is_undergrad_c2 or
                notice.is_fyp or notice.is_past_student or
                notice.is_clinician or notice.is_employee or
                notice.is_faculty or notice.is_instructor or
                notice.is_past_employee or notice.is_retiree or
                notice.is_staff_employee or notice.is_stud_employee or
                notice.is_intl_stud)


def student_affiliation_matched(notice, affiliations):
    return (notice.is_applicant and affiliations["applicant"] or
            notice.is_grad and affiliations["grad"] or
            notice.is_grad_c2 and affiliations["grad_c2"] or
            notice.is_intl_stud and affiliations["intl_stud"] or
            notice.is_pce and affiliations["pce"] or
            notice.is_student and affiliations["student"] or
            notice.is_undergrad and affiliations["undergrad"] or
            notice.is_undergrad_c2 and affiliations["undergrad_c2"] or
            notice.is_past_student and affiliations["past_stud"] or
            notice.is_fyp and affiliations["fyp"] or
            notice.is_alumni and affiliations["alumni"])


def employee_affiliation_matched(notice, affiliations):
    keys = ["clinician", "employee", "faculty", "instructor",
            "staff_employee", "stud_employee", "past_employee", "retiree"]
    for key in keys:
        if getattr(notice, "is_" + key) and affiliations[key]:
            return True
    return False
