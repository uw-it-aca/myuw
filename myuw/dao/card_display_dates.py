"""
Generates the booleans to determine card visibility,
based on dates in either the current, next, or previous term.
https://docs.google.com/document/d/14q26auOLPU34KFtkUmC_bkoo5dAwegRzgpwmZEQMhaU
"""

import logging
from datetime import datetime, timedelta
from myuw.logger.logresp import log_exception
from myuw.dao.term import get_comparison_datetime,\
    get_current_quarter, get_next_quarter, get_previous_quarter,\
    get_term_after, is_in_summer_quarter,\
    is_in_summer_b_term, get_bod_current_term_class_start,\
    get_eod_current_term_last_instruction, get_bod_7d_before_last_instruction,\
    get_eod_7d_after_class_start, get_eod_current_term_last_final_exam
from myuw.dao.term import get_bod_class_start_quarter_after as\
    get_bod_quarter_after
from myuw.dao.iasystem import in_coursevel_fetch_window


logger = logging.getLogger(__name__)


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
    reg_data = get_reg_data(now, request)
    data = {
        "is_after_7d_before_last_instruction":
            is_after_7d_before_last_instruction(now, request),
        "is_after_grade_submission_deadline":
            is_before_bof_term(now, request),
        "is_after_last_day_of_classes":
            not is_before_last_day_of_classes(now, request),
        "is_after_start_of_registration_display_period":
            reg_data["after_start"],
        "is_after_start_of_summer_reg_display_period1":
            reg_data["after_summer1_start"],
        "is_after_start_of_summer_reg_display_periodA":
            reg_data["after_summerA_start"],
        "is_before_eof_7days_of_term":
            is_before_eof_7d_after_class_start(now, request),
        "is_before_end_of_finals_week":
            is_before_eof_finals_week(now, request),
        "is_before_end_of_registration_display_period":
            reg_data["after_start"],
        "is_before_end_of_summer_reg_display_periodA":
            reg_data["after_summerA_start"],
        "is_before_end_of_summer_reg_display_period1":
            reg_data["after_summer1_start"],
        "is_before_first_day_of_term":
            is_before_bof_term(now, request),
        "is_before_last_day_of_classes":
            is_before_last_day_of_classes(now, request),
        "myplan_peak_load": during_myplan_peak_load(now, request),
        "reg_period1_started": reg_data["period1_started"],
        "is_summer": is_in_summer_quarter(request),
        "is_after_summer_b": is_in_summer_b_term(request),
        "in_coursevel_fetch_window": in_coursevel_fetch_window(request),
        "comparison_date": get_comparison_datetime(request)
    }
    try:
        last_term = get_previous_quarter(request)
        data["current_summer_term"] = "{},summer".format(last_term.year)
        data["last_term"] = "{},{}".format(last_term.year, last_term.quarter)
    except Exception:
        log_exception(logger, 'get_previous_quarter',
                      traceback.format_exc(chain=False))
    return data


def is_before_bof_term(now, request):
    """
    The term switches after the grade submission deadline.
    @return true if it is before the begining of the 1st day of instruction
    """
    logger.debug("{} is_before_bof_term {} ==> {}".format(
        now, get_bod_current_term_class_start(request),
        now < get_bod_current_term_class_start(request)))
    return now < get_bod_current_term_class_start(request)


def is_before_eof_7d_after_class_start(now, request):
    """
    @return true if it is before the end of the 7 days
    after the instruction start day
    """
    logger.debug("{} is_before_eof_7d_after_class_start {} ==> {}".format(
        now, get_eod_7d_after_class_start(request),
        now < get_eod_7d_after_class_start(request)))
    return now < get_eod_7d_after_class_start(request)


def is_after_7d_before_last_instruction(now, request):
    """
    @return true if it is after the begining of 7 days
    before instruction end
    """
    logger.debug("{} is_after_7d_before_last_instruction {} ==> {}".format(
        now, get_bod_7d_before_last_instruction(request),
        now > get_bod_7d_before_last_instruction(request)))
    return now > get_bod_7d_before_last_instruction(request)


def is_before_last_day_of_classes(now, request):
    """
    @return true if it is before the end of the last day of classes
    """
    logger.debug("{} is_before_last_day_of_classes {} ==> {}".format(
        now, get_eod_current_term_last_instruction(request),
        now < get_eod_current_term_last_instruction(request)))
    return now < get_eod_current_term_last_instruction(request)


def is_before_eof_finals_week(now, request):
    """
    @return true if it is before the end of the last day of finalsweek
    """
    logger.debug("{} is_before_eof_finals_week {} ==> {}".format(
        now, get_eod_current_term_last_final_exam(request),
        now < get_eod_current_term_last_final_exam(request)))
    return now < get_eod_current_term_last_final_exam(request)


def during_myplan_peak_load(now, request):
    reg_data = get_reg_data(now, request)
    logger.debug("{} myplan_peak_load ==> {}".format(
        now, reg_data["myplan_peak_load"]))
    return reg_data["myplan_peak_load"]


def get_reg_data(now, request):
    """
    now is the second after mid-night
    """
    if hasattr(request, "myuw_reg_data"):
        return request.myuw_reg_data
    term_reg_data = {
        "after_start": False,
        "after_summer1_start": False,
        "after_summerA_start": False,
        "period1_started": False,
        "myplan_peak_load": False
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
    request.myuw_reg_data = term_reg_data
    return term_reg_data


def is_term_myplan_peak(now, term, data):
    now_date = now.date()
    if (now_date >= term.registration_period1_start and
            now_date <= term.registration_period1_end):
        peak_start_time = datetime(now.year, now.month, now.day, 5, 30, 0)
        peak_end_time = datetime(now.year, now.month, now.day, 6, 30, 0)
        if (now >= peak_start_time and now <= peak_end_time):
            return True
    return False


def get_term_reg_data(now, term, data):
    if term.registration_period1_start is None:
        data["myplan_peak_load"] = False
        return

    if not (data["myplan_peak_load"] is True):
        data["myplan_peak_load"] = is_term_myplan_peak(now, term, data)

    now = now.date()
    if term.quarter == "summer":
        if now >= term.registration_period1_start - timedelta(days=7) and\
                now < term.registration_period1_start + timedelta(days=7):
            data["after_summerA_start"] = True
            data["before_summerA_end"] = True
            if now >= term.registration_period1_start:
                data["period1_started"] = True

        elif now >= term.registration_period1_start + timedelta(days=7) and\
                now < term.registration_period2_start + timedelta(days=7):
            data["after_summer1_start"] = True
            data["before_summer1_end"] = True
            if now >= term.registration_period1_start:
                data["period1_started"] = True
    else:
        if now >= term.registration_period1_start - timedelta(days=14) and\
                now < term.registration_period2_start + timedelta(days=7):
            data["after_start"] = True
            data["before_end"] = True
            if now >= term.registration_period1_start:
                data["period1_started"] = True


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
           'myplan_peak_load': 'myplan_peak_load',
           'myuw_in_coursevel_fetch_window': 'in_coursevel_fetch_window'
           }

    for key in MAP:
        if key in request.session:
            values[MAP[key]] = request.session[key]
