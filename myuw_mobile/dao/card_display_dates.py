"""
Generates the 7 booleans used to determine card visibility, based on dates in
either the current, next, or previous term.

https://docs.google.com/document/d/14q26auOLPU34KFtkUmC_bkoo5dAwegRzgpwmZEQMhaU
"""

from restclients.sws import term
from django.conf import settings
from datetime import datetime, timedelta
from myuw_mobile.dao.term import get_comparison_date, get_current_quarter
from myuw_mobile.dao.term import get_next_quarter
from restclients.sws.term import get_term_after, get_term_before


def get_card_visibilty_date_values(request=None):
    now = get_comparison_date(request)
    n2 = datetime(now.year, now.month, now.day, 0, 0, 0)
    values = get_values_by_date(n2, request)
    set_js_overrides(request, values)
    return values


def get_values_by_date(now, request):
    current_term = get_current_quarter(request)
    next_term = get_next_quarter(request)
    term_after_next = get_term_after(next_term)

    is_after_grade_submission_deadline = False
    is_after_last_day_of_classes = False
    is_after_start_of_registration_display_period = False
    is_after_start_of_summer_reg_display_period1 = False
    is_after_start_of_summer_reg_display_periodA = False
    is_before_end_of_finals_week = False
    is_before_last_day_of_classes = False
    is_before_end_of_registration_display_period = False
    is_before_end_of_summer_reg_display_period1 = False
    is_before_end_of_summer_reg_display_periodA = False
    is_before_first_day_of_term = False

    if now.date() < current_term.first_day_quarter:
        is_before_first_day_of_term = True
        # We need to see if we're before this term's 1st day - the term
        # switches at the grade submission deadline.
        is_after_grade_submission_deadline = True

    raw_date = current_term.last_day_instruction
    d = datetime(raw_date.year, raw_date.month, raw_date.day)
    if now >= d + timedelta(days=1):
        is_after_last_day_of_classes = True

    term_reg_data = {
        "after_start": False,
        "after_summer1_start": False,
        "after_summerA_start": False,
    }

    get_reg_data(now, next_term, term_reg_data)
    # We also need to be able to show this term's registration stuff, because
    # the period 2 stretches past the grade submission deadline
    get_reg_data(now, current_term, term_reg_data)
    # We also need to be able to show the term after next, in spring quarter
    get_reg_data(now, term_after_next, term_reg_data)

    if term_reg_data["after_start"]:
        is_after_start_of_registration_display_period = True
        is_before_end_of_registration_display_period = True

    if term_reg_data["after_summer1_start"]:
        is_after_start_of_summer_reg_display_period1 = True
        is_before_end_of_summer_reg_display_period1 = True

    if term_reg_data["after_summerA_start"]:
        is_after_start_of_summer_reg_display_periodA = True
        is_before_end_of_summer_reg_display_periodA = True

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
    before_reg_end = is_before_end_of_registration_display_period

    summerA_start = is_after_start_of_summer_reg_display_periodA
    summer1_start = is_after_start_of_summer_reg_display_period1

    summerA_end = is_before_end_of_summer_reg_display_periodA
    summer1_end = is_before_end_of_summer_reg_display_period1

    last_term = get_term_before(current_term)
    return {
        "is_after_grade_submission_deadline": after_submission,
        "is_after_last_day_of_classes": is_after_last_day_of_classes,
        "is_after_start_of_registration_display_period": after_registration,
        "is_after_start_of_summer_reg_display_periodA": summerA_start,
        "is_after_start_of_summer_reg_display_period1": summer1_start,
        "is_before_end_of_finals_week": is_before_end_of_finals_week,
        "is_before_last_day_of_classes": is_before_last_day_of_classes,
        "is_before_end_of_registration_display_period": before_reg_end,
        "is_before_end_of_summer_reg_display_periodA": summerA_end,
        "is_before_end_of_summer_reg_display_period1": summer1_end,
        "is_before_first_day_of_term": is_before_first_day_of_term,
        "last_term": "%s,%s" % (last_term.year, last_term.quarter),
    }


def get_reg_data(now, term, data):
    if term.quarter == "summer":
        if (now >= term.registration_period1_start - timedelta(days=7) and
                now < term.registration_period1_start + timedelta(days=7)):
            data["after_summerA_start"] = True
            data["before_summerA_end"] = True

        elif (now >= term.registration_period1_start + timedelta(days=7) and
                now < term.registration_period2_start + timedelta(days=7)):
            data["after_summer1_start"] = True
            data["before_summer1_end"] = True
    else:
        if (now >= term.registration_period1_start - timedelta(days=14) and
                now < term.registration_period2_start + timedelta(days=7)):
            data["after_start"] = True
            data["before_end"] = True


def set_js_overrides(request, values):
    after_reg = 'is_after_start_of_registration_display_period'
    before_reg = 'is_before_end_of_registration_display_period'
    MAP = {'myuw_after_submission': 'is_after_grade_submission_deadline',
           'myuw_after_last_day': 'is_after_last_day_of_classes',
           'myuw_after_reg': after_reg,
           'myuw_before_finals_end': 'is_before_end_of_finals_week',
           'myuw_before_last_day': 'is_before_last_day_of_classes',
           'myuw_before_end_of_reg_display': before_reg,
           'myuw_before_first_day': 'is_before_first_day_of_term',
           }

    for key, value in MAP.iteritems():
        if key in request.session:
            values[value] = request.session[key]
