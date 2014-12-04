"""
Generates the 7 booleans used to determine card visibility, based on dates in
either the current, next, or previous term.

https://docs.google.com/document/d/14q26auOLPU34KFtkUmC_bkoo5dAwegRzgpwmZEQMhaU
"""

from restclients.sws import term
from django.conf import settings
from datetime import datetime, timedelta


def get_card_visibilty_date_values():
    current_term = term.get_current_term()

    # Doing this instead of get_next/get_previous,
    # because of this in get_current_term:
    # if datetime.now() > term.grade_submission_deadline:
    #     return get_next_term()
    last_term = term.get_term_before(current_term)
    next_term = term.get_term_after(current_term)

    is_after_grade_submission_deadline = False
    is_after_last_day_of_classes = False
    is_after_start_of_registration_display_period = False
    is_before_first_day_of_current_term = False
    is_before_end_of_finals_week = False
    is_before_last_day_of_classes = False
    is_before_end_of_registration_display_period = False

    now = get_comparison_date()

    if now > last_term.grade_submission_deadline:
        is_after_start_of_registration_display_period = True

    raw_date = current_term.last_day_instruction
    d = datetime(raw_date.year, raw_date.month, raw_date.day)
    if now >= d + timedelta(days=1):
        is_after_last_day_of_classes = True

    # XXX - this will be a bug when summer quarter comes around
    # because there will need to be a summer term + a next non-summer term
    # version of this.  We're holding off on the summer term card though...
    if now - timedelta(days=7) > next_term.registration_services_start:
        is_after_start_of_registration_display_period = True

    if now < next_term.registration_period2_start + timedelta(days=7):
        is_before_end_of_registration_display_period = True

    raw_date = current_term.first_day_quarter
    d = datetime(raw_date.year, raw_date.month, raw_date.day)
    if now < d:
        is_before_first_day_of_current_term = True

    raw_date = current_term.last_final_exam_date
    d = datetime(raw_date.year, raw_date.month, raw_date.day)
    if now < d:
        is_before_end_of_finals_week = True

    raw_date = current_term.last_day_instruction
    d = datetime(raw_date.year, raw_date.month, raw_date.day)
    if now < d + timedelta(days=1):
        is_before_last_day_of_classes = True

    after_submission = is_after_grade_submission_deadline
    after_registration = is_after_start_of_registration_display_period
    before_first = is_before_first_day_of_current_term
    before_reg_end = is_before_end_of_registration_display_period
    return {
        "is_after_grade_submission_deadline": after_submission,
        "is_after_last_day_of_classes": is_after_last_day_of_classes,
        "is_after_start_of_registration_display_period": after_registration,
        "is_before_first_day_of_current_term": before_first,
        "is_before_end_of_finals_week": is_before_end_of_finals_week,
        "is_before_last_day_of_classes": is_before_last_day_of_classes,
        "is_before_end_of_registration_display_period": before_reg_end,
    }


def get_comparison_date():
    """
    Allows us to pretend we're at various points in the term,
    so we can test against live data sources at various points in the year.
    """

    override_date = getattr(settings, "MYUW_CARD_DISPLAY_DATE_OVERRIDE", None)

    if override_date:
        return datetime.strptime(override_date, "%Y-%m-%d")

    return datetime.now()
