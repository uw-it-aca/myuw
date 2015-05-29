"""
Generates the booleans to determine card visibility,
based on dates in either the current, next, or previous term.
https://docs.google.com/document/d/14q26auOLPU34KFtkUmC_bkoo5dAwegRzgpwmZEQMhaU
"""

from django.conf import settings
from datetime import datetime, timedelta
from myuw_mobile.dao.term import get_comparison_date,\
    get_current_quarter, get_next_quarter,\
    get_term_after, get_term_before, get_bof_1st_instruction,\
    get_eof_last_instruction, get_bof_7d_before_last_instruction,\
    get_eof_7d_after_class_start, get_eof_last_final_exam


def get_card_visibilty_date_values(request=None):
    now = get_comparison_date(request)
    after_midnight = datetime(now.year, now.month, now.day,
                              0, 0, 1)
    values = get_values_by_date(after_midnight, request)
    set_js_overrides(request, values)
    return values


def get_values_by_date(now, request):
    """
    now is a datetime object of 1 second after the beginning of the day.
    """
    current_term = get_current_quarter(request)
    next_term = get_next_quarter(request)
    term_after_next = get_term_after(next_term)

    # the term switches after the grade submission deadline.
    is_before_first_day_of_term = \
        now < get_bof_1st_instruction(request)
    is_after_grade_submission_deadline = is_before_first_day_of_term

    is_before_eof_7d_after_class_start = \
        now < get_eof_7d_after_class_start(request)

    is_after_7d_before_last_instruction = \
        now > get_bof_7d_before_last_instruction(request)

    is_before_last_day_of_classes = \
        now < get_eof_last_instruction(request)

    is_after_last_day_of_classes = not is_before_last_day_of_classes

    is_before_eof_finals_week = \
        now < get_eof_last_final_exam(request)

    term_reg_data = {
        "after_start": False,
        "after_summer1_start": False,
        "after_summerA_start": False,
    }
    get_reg_data(now, next_term, term_reg_data)
    # We need to show this term's registration stuff, because
    # the period 2 stretches past the grade submission deadline
    get_reg_data(now, current_term, term_reg_data)
    # We also need to be able to show the term after next, in spring quarter
    get_reg_data(now, term_after_next, term_reg_data)

    is_after_start_of_registration_display_period = False
    is_after_start_of_summer_reg_display_period1 = False
    is_after_start_of_summer_reg_display_periodA = False
    is_before_end_of_registration_display_period = False
    is_before_end_of_summer_reg_display_period1 = False
    is_before_end_of_summer_reg_display_periodA = False

    if term_reg_data["after_start"]:
        is_after_start_of_registration_display_period = True
        is_before_end_of_registration_display_period = True

    if term_reg_data["after_summer1_start"]:
        is_after_start_of_summer_reg_display_period1 = True
        is_before_end_of_summer_reg_display_period1 = True

    if term_reg_data["after_summerA_start"]:
        is_after_start_of_summer_reg_display_periodA = True
        is_before_end_of_summer_reg_display_periodA = True

    last_term = get_term_before(current_term)
    return {
        "is_after_grade_submission_deadline":
            is_after_grade_submission_deadline,
        "is_after_last_day_of_classes":
            is_after_last_day_of_classes,
        "is_after_start_of_registration_display_period":
            is_after_start_of_registration_display_period,
        "is_after_start_of_summer_reg_display_periodA":
            is_after_start_of_summer_reg_display_periodA,
        "is_after_start_of_summer_reg_display_period1":
            is_after_start_of_summer_reg_display_period1,
        "is_before_end_of_finals_week": is_before_eof_finals_week,
        "is_before_last_day_of_classes": is_before_last_day_of_classes,
        "is_before_end_of_registration_display_period":
            is_before_end_of_registration_display_period,
        "is_before_end_of_summer_reg_display_periodA":
            is_before_end_of_summer_reg_display_periodA,
        "is_before_end_of_summer_reg_display_period1":
            is_before_end_of_summer_reg_display_period1,
        "is_before_first_day_of_term": is_before_first_day_of_term,
        "is_before_eof_7days_of_term": is_before_eof_7d_after_class_start,
        "last_term": "%s,%s" % (last_term.year, last_term.quarter),
        "is_after_7d_before_last_instruction":
            is_after_7d_before_last_instruction
    }


def get_reg_data(now, term, data):
    """
    now is the second after mid-night
    """
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
           'myuw_before_end_of_first_week': 'is_before_eof_7days_of_term',
           'myuw_after_eval_start': 'is_after_7d_before_last_instruction'
           }

    for key, value in MAP.iteritems():
        if key in request.session:
            values[value] = request.session[key]
