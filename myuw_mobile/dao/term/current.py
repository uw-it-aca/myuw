"""
This module provides access of term data
related to the request.
"""

from datetime import date, datetime, timedelta
import logging
import traceback
from myuw_mobile.dao.term import get_current_quarter, get_next_quarter,\
    convert_date_to_datetime, get_specific_quarter, is_a_term, is_b_term,\
    is_half_summer_term, is_full_summer_term, is_same_summer_term,\
    get_comparison_date


logger = logging.getLogger(__name__)


def get_current_summer_term(request):
    """
    Return a string of the current summer a-term or b-term
    or None if it is not a summer quarter
    """
    if not is_summer_term(request):
        return None
    aterm_last_date = get_current_quarter(request).aterm_last_date
    if get_comparison_date(request) > aterm_last_date:
        return "b-term"
    else:
        return "a-term"


def get_next_non_summer_quarter(request):
    term = get_next_quarter(request)
    if term.quarter == "summer":
        return get_next_autumn_quarter(request)

    return term


def get_next_autumn_quarter(request):
    """
    Return the Term object for the next autumn quarter in the same year
    when in the Spring quarter
    """
    return get_specific_quarter(get_current_quarter(request).year, 'autumn')


def term_matched(request, given_summer_term):
    """
    @return true if this is not a summer quarter or
    the given_summer_term is overlaped with the current summer term
    """
    current_summer_term = get_current_summer_term(request)
    if given_summer_term is None or current_summer_term is None:
        return True
    return (is_same_summer_term(current_summer_term, given_summer_term) or
            is_full_summer_term(given_summer_term) and
            is_b_term(current_summer_term))


def is_summer_term(request):
    """
    Return True if it is currently in a summer quarter
    """
    term = get_current_quarter(request)
    return term.quarter == "summer"


def is_in_summer_a_term(request):
    """
    @return true if it is in a summer quarter, A-term
    """
    return is_a_term(get_current_summer_term(request))


def is_in_summer_b_term(request):
    """
    @return true if it is in a summer quarter, B-term
    """
    return is_b_term(get_current_summer_term(request))


def get_eof_summer_aterm(request):
    """
    @return the datetime (or date if to_datetime is False )object
    of the end of the summer quarter A-term
    (it is also the beginning of summer B-term).
    If it is currently not a summer term, return None.
    """
    if not is_in_summer_a_term(request):
        return None
    aterm_last_date = get_current_quarter(request).aterm_last_date
    return convert_date_to_datetime(aterm_last_date + timedelta(days=1))


def get_eof_last_instruction(request, break_at_a_term=False):
    """
    @return the datetime object of the end of the last instruction day
    for current quarter and current summer A-term if applicable
    """
    eof_aterm_last_day = get_eof_summer_aterm(request)
    if break_at_a_term and eof_aterm_last_day is not None:
        return eof_aterm_last_day
    return convert_date_to_datetime(
        get_current_quarter(request).last_day_instruction +
        timedelta(days=1))


def get_bof_7d_before_last_instruction(request):
    """
    @return the datetime object of the beginning of
    the 7 days before the last instruction day for
    current quarter and current summer-term if applicable.
    Exclude the last instruction day.
    """
    return get_eof_last_instruction(request, True) - timedelta(days=8)


def get_bof_1st_instruction(request, break_at_a_term=False):
    """
    @return the datetime object of the begining of quarter start day
    or the beginning of summer B-term if applicable
    """
    eof_aterm_last_day = get_eof_summer_aterm(request)
    if break_at_a_term and eof_aterm_last_day is not None:
        # the beginning of summer B-term
        return eof_aterm_last_day
    return convert_date_to_datetime(
        get_current_quarter(request).first_day_quarter)


def get_eof_7d_after_class_start(request, break_at_a_term=False):
    """
    @return the datetime object of seven days after the first day for
    current quarter. Exclude the first instruction day.
    """
    return get_bof_1st_instruction(request, break_at_a_term) +\
        timedelta(days=8)


def get_eof_term(request, break_at_a_term=False):
    """
    @return the datetime object of the end of the grade submission
    deadline or the end of summer a-term if applicable
    """
    eof_aterm_last_day = get_eof_summer_aterm(request)
    if break_at_a_term and eof_aterm_last_day is not None:
        return eof_aterm_last_day
    return convert_date_to_datetime(
        get_current_quarter(request).grade_submission_deadline.date() +
        timedelta(days=1))


def get_eof_next_term(request):
    """
    @return the datetime object of the end of the grade submission
    deadline of the following term
    """
    return convert_date_to_datetime(
        get_next_quarter(request).grade_submission_deadline.date() +
        timedelta(days=1))


def get_eof_last_final_exam(request, break_at_a_term=False):
    """
    @return the datetime object of the current quarter
    the end of the last final exam day
    """
    eof_aterm_last_day = get_eof_summer_aterm(request)
    if break_at_a_term and eof_aterm_last_day is not None:
        return eof_aterm_last_day
    return convert_date_to_datetime(
        get_current_quarter(request).last_final_exam_date +
        timedelta(days=1))
