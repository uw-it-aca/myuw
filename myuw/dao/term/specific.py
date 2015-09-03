"""
This module provides access of term data
related to a specific year and quarter.
"""

from datetime import date, datetime, timedelta
import logging
import traceback
from myuw.dao.term import get_current_quarter, get_next_quarter,\
    get_specific_quarter, convert_date_to_datetime, get_term_after


logger = logging.getLogger(__name__)


def get_eof_term(term):
    """
    Return the datetime object of the end of grade submission deadline
    for the given term.
    Only the summer full term is relevant.
    """
    return convert_date_to_datetime(term.grade_submission_deadline.date() +
                                    timedelta(days=1))


def get_eof_term_yq(year, quarter):
    """
    Return the datetime object of the end of grade submission deadline
    for the term of the give year and quarter.
    Only the summer full term is relevant.
    """
    return get_eof_term(get_specific_quarter(year, quarter))


def get_eof_last_instruction(term):
    """
    Return the datetime object of the end of last instruction
    for the given term.
    Only the summer full term is relevant.
    """
    return convert_date_to_datetime(term.last_day_instruction +
                                    timedelta(days=1))


def get_eof_last_instruction_yq(year, quarter):
    """
    Return the datetime object of the end of last instruction
    for the term of the give year and quarter.
    Only the summer full term is relevant.
    """
    return get_eof_last_instruction(get_specific_quarter(year, quarter))


def get_eof_term_after(term):
    """
    Return the datetime object of the end of the term after the given term.
    Only the summer full term is relevant.
    """
    return convert_date_to_datetime(
        get_term_after(term).grade_submission_deadline.date() +
        timedelta(days=1))


def get_eof_term_after_yq(year, quarter):
    """
    Return the datetime object of the end of the term after the given term.
    Only the summer full term is relevant.
    """
    return get_eof_term_after(get_specific_quarter(year, quarter))


def get_first_day_term_after(term):
    """
    Return the datetime object of the beginning of
    the first day in the term after the give year and quarter.
    Only the summer full term is relevant.
    """
    return convert_date_to_datetime(get_term_after(term).first_day_quarter)


def get_first_day_term_after_yq(year, quarter):
    """
    Return the datetime object of the beginning of
    the first day in the term after the give year and quarter.
    Only the summer full term is relevant.
    """
    return get_first_day_term_after(get_specific_quarter(year, quarter))
