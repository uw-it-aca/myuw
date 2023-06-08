# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from datetime import timedelta
from django.db.models import Q
from restclients_core.exceptions import DataFailureException
from myuw.dao import log_err
from myuw.dao.affiliation import get_all_affiliations
from myuw.models.myuw_notice import (
    MyuwNotice, start_week_range, duration_range)
from myuw.dao.gws import is_effective_member
from myuw.dao.term import (
    get_current_quarter, get_comparison_date,
    get_comparison_datetime_with_tz)

logger = logging.getLogger(__name__)


def get_myuw_notices_for_user(request):
    date_notices = get_notices_by_date(request)
    term_notices = get_notices_by_term(request)
    affiliations = get_all_affiliations(request)

    user_notices = []
    for notice in (date_notices + term_notices):

        if notice.has_target_group():
            try:
                if is_effective_member(request, notice.target_group):
                    user_notices.append(notice)
            except DataFailureException:
                log_err(
                    logger, "is_effective_member of target group({})".format(
                        notice.target_group), traceback, request)
                # notice skipped
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
                notice.is_grad or notice.is_grad_c2 or notice.is_pce or
                notice.is_intl_stud or notice.not_intl_stud or
                notice.is_past_student or notice.is_student or
                notice.is_undergrad or notice.is_undergrad_c2 or
                notice.is_clinician or notice.is_employee or
                notice.is_faculty or notice.is_instructor or
                notice.is_past_employee or notice.is_retiree or
                notice.is_staff_employee or notice.is_stud_employee)


def student_affiliation_matched(notice, affiliations):
    return (notice.is_alumni and affiliations["alumni"] or
            notice.is_applicant and affiliations["applicant"] or
            notice.is_grad and affiliations["grad"] or
            notice.is_grad_c2 and affiliations["grad_c2"] or
            notice.is_intl_stud and affiliations["intl_stud"] or
            notice.is_past_student and affiliations["past_stud"] or
            notice.is_pce and affiliations["pce"] or
            notice.is_student and affiliations["student"] or
            notice.is_undergrad and affiliations["undergrad"] or
            notice.is_undergrad_c2 and affiliations["undergrad_c2"]) and (
            not (notice.not_intl_stud and affiliations["intl_stud"]))


def employee_affiliation_matched(notice, affiliations):
    keys = ["clinician", "employee", "faculty", "instructor",
            "staff_employee", "stud_employee", "past_employee", "retiree"]
    for key in keys:
        if getattr(notice, "is_" + key) and affiliations[key]:
            return True
    return False


def get_notices_by_date(request):
    selected_notices = []
    date = get_comparison_datetime_with_tz(request)
    fetched_notices = MyuwNotice.objects.filter(start__lte=date)
    for notice in fetched_notices:
        if notice.end is not None and date < notice.end:
            selected_notices.append(notice)
    return selected_notices


def get_notices_by_term(request):
    # MUWM-5265
    selected_notices = []
    cur_term = get_current_quarter(request)
    cmp_date = get_comparison_date(request)
    if cur_term.is_summer_quarter():
        fetched_term_notices = MyuwNotice.objects.filter(
            Q(is_summer_a=True) | Q(is_summer_b=True))
    else:
        fltr = {"is_{}".format(cur_term.quarter.lower()): True}
        fetched_term_notices = MyuwNotice.objects.filter(**fltr)

    for notice in fetched_term_notices:
        if (notice.start_week in start_week_range and
                notice.duration in duration_range):
            start_sunday = get_prev_sunday(
                get_first_day_quarter(cur_term, notice))
            start_date = get_start_date(start_sunday, notice.start_week)
            end_date = start_date + timedelta(weeks=notice.duration)
            if start_date <= cmp_date < end_date:
                selected_notices.append(notice)
    return selected_notices


def get_first_day_quarter(cur_term, notice):
    if notice.is_summer_b:
        return cur_term.bterm_first_date
    return cur_term.first_day_quarter


def get_prev_sunday(first_day_quarter):
    week_day_idx = (first_day_quarter.weekday() + 1) % 7
    # Sunday is 0 and Saturday is 6
    return first_day_quarter - timedelta(days=week_day_idx)


def get_start_date(start_sunday, notice_start_week):
    return start_sunday + timedelta(weeks=notice_start_week)
