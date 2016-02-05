"""
Generates the booleans to determine card visibility,
based on dates in either the current, next, or previous term.
https://docs.google.com/document/d/14q26auOLPU34KFtkUmC_bkoo5dAwegRzgpwmZEQMhaU
"""

from django.conf import settings
from datetime import datetime, timedelta
from myuw.dao.term import get_comparison_datetime,\
    get_current_quarter, get_next_quarter, get_previous_quarter,\
    get_term_after, is_in_summer_quarter,\
    is_in_summer_b_term, get_bod_current_term_class_start,\
    get_eod_current_term_last_instruction, get_bod_7d_before_last_instruction,\
    get_eod_7d_after_class_start, get_eod_current_term_last_final_exam
from myuw.dao.term import get_bod_class_start_quarter_after as\
    get_bod_quarter_after
from myuw.dao.iasystem import in_coursevel_fetch_window


def in_show_grades_period(term, request):
    return (term is not None and request is not None and
            get_comparison_datetime(request) < get_bod_quarter_after(term))


def get_card_visibilty_date_values(request=None):
    values = get_values_by_date(get_comparison_datetime(request),
                                request)
    set_js_overrides(request, values)
    return values


def get_values_by_date(now, request):
    """
    now is a datetime object of 1 second after the beginning of the day.
    """
    if get_current_quarter(request) is None:
        return None

    last_term = get_previous_quarter(request)

    return {
        "is_after_7d_before_last_instruction":
            is_after_7d_before_last_instruction(now, request),
        "is_after_grade_submission_deadline":
            is_before_bof_term(now, request),
        "is_after_last_day_of_classes":
            is_after_last_day_of_classes(now, request),
        "is_after_start_of_registration_display_period":
            is_after_bof_and_before_eof_reg_period(now, request),
        "is_after_start_of_summer_reg_display_period1":
            is_after_bof_and_before_eof_summer_reg_period1(now, request),
        "is_after_start_of_summer_reg_display_periodA":
            is_after_bof_and_before_eof_summer_reg_periodA(now, request),
        "is_before_eof_7days_of_term":
            is_before_eof_7d_after_class_start(now, request),
        "is_before_end_of_finals_week":
            is_before_eof_finals_week(now, request),
        "is_before_end_of_registration_display_period":
            is_after_bof_and_before_eof_reg_period(now, request),
        "is_before_end_of_summer_reg_display_periodA":
            is_after_bof_and_before_eof_summer_reg_periodA(now, request),
        "is_before_end_of_summer_reg_display_period1":
            is_after_bof_and_before_eof_summer_reg_period1(now, request),
        "is_before_first_day_of_term":
            is_before_bof_term(now, request),
        "is_before_last_day_of_classes":
            is_before_last_day_of_classes(now, request),
        "is_summer": is_in_summer_quarter(request),
        "is_after_summer_b": is_in_summer_b_term(request),
        "current_summer_term": "%s,%s" % (last_term.year, "summer"),
        "last_term": "%s,%s" % (last_term.year, last_term.quarter),
        "in_coursevel_fetch_window": in_coursevel_fetch_window(request),
    }


def is_before_bof_term(now, request):
    """
    The term switches after the grade submission deadline.
    @return true if it is before the begining of the 1st day of instruction
    """
    return now < get_bod_current_term_class_start(request)


def is_before_eof_7d_after_class_start(now, request):
    """
    @return true if it is before the end of the 7 days
    after the instruction start day
    """
    return now < get_eod_7d_after_class_start(request)


def is_after_7d_before_last_instruction(now, request):
    """
    @return true if it is after the begining of 7 days
    before instruction end
    """
    return now > get_bod_7d_before_last_instruction(request)


def is_before_last_day_of_classes(now, request):
    """
    @return true if it is before the end of the last day of classes
    """
    return now < get_eod_current_term_last_instruction(request)


def is_after_last_day_of_classes(now, request):
    """
    @return true if it is on or after the last day of classes
    """
    return not is_before_last_day_of_classes(now, request)


def is_before_eof_finals_week(now, request):
    """
    @return true if it is before the end of the last day of finalsweek
    """
    return now < get_eod_current_term_last_final_exam(request)


def is_after_bof_and_before_eof_reg_period(now, request):
    """
    @return true if it is after the begining of registration display period,
    and before the end of registration display period.
    """
    reg_data = get_reg_data(now, request)
    return reg_data["after_start"]


def is_after_bof_and_before_eof_summer_reg_period1(now, request):
    """
    @return true if it is after the begining of registration display period1,
    and before the end of registration display period1.
    """
    reg_data = get_reg_data(now, request)
    return reg_data["after_summer1_start"]


def is_after_bof_and_before_eof_summer_reg_periodA(now, request):
    """
    @return true if it is after the begining of registration display periodA,
    and before the end of registration display periodA.
    """
    reg_data = get_reg_data(now, request)
    return reg_data["after_summerA_start"]


def get_reg_data(now, request):
    """
    now is the second after mid-night
    """
    term_reg_data = {
        "after_start": False,
        "after_summer1_start": False,
        "after_summerA_start": False,
    }
    next_term = get_next_quarter(request)
    get_term_reg_data(now, next_term, term_reg_data)
    # We need to show this term's registration stuff, because
    # the period 2 stretches past the grade submission deadline
    current_term = get_current_quarter(request)
    get_term_reg_data(now, current_term, term_reg_data)
    # We also need to be able to show the term after next, in spring quarter
    term_after_next = get_term_after(next_term)
    get_term_reg_data(now, term_after_next, term_reg_data)
    return term_reg_data


def get_term_reg_data(now, term, data):
    if term.quarter == "summer":
        if now >= term.registration_period1_start - timedelta(days=7) and\
                now < term.registration_period1_start + timedelta(days=7):
            data["after_summerA_start"] = True
            data["before_summerA_end"] = True

        elif now >= term.registration_period1_start + timedelta(days=7) and\
                now < term.registration_period2_start + timedelta(days=7):
            data["after_summer1_start"] = True
            data["before_summer1_end"] = True
    else:
        if now >= term.registration_period1_start - timedelta(days=14) and\
                now < term.registration_period2_start + timedelta(days=7):
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
           'myuw_after_eval_start': 'is_after_7d_before_last_instruction',
           'myuw_in_coursevel_fetch_window': 'in_coursevel_fetch_window'
           }

    for key, value in MAP.iteritems():
        if key in request.session:
            values[value] = request.session[key]
