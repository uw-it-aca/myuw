"""
This module encapsulates the access of the term data
(including registered summer terms, registered future terms).
"""

from datetime import date, datetime, timedelta
import logging
import traceback
from django.conf import settings
import restclients.sws.term as sws_term
from restclients.dao import SWS_DAO
from restclients.sws.term import get_term_by_date, get_term_after
from restclients.sws.term import get_term_before, get_current_term
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception


logger = logging.getLogger(__name__)


def get_comparison_date(request):
    """
    To test at various points in the year,
    overrides to the date if specified in the request
    otherwise return the default date.
    """
    FORMAT = "%Y-%m-%d"

    override_date = None
    if request:
        if "myuw_override_date" in request.session:
            try:
                val = request.session["myuw_override_date"]
                test_date = datetime.strptime(val, FORMAT)
                override_date = val
            except Exception as ex:
                pass

    if override_date:
        return datetime.strptime(override_date, "%Y-%m-%d").date()

    return get_default_date()


def get_default_date():
    """
    A hook to help with mock data testing - put the default date
    right in the middle of the "current" term.
    """
    if is_using_file_dao():
        term = get_current_term()
        first_day = term.first_day_quarter

        return first_day + timedelta(days=14)
    return datetime.now().date()


def is_using_file_dao():
    dao = SWS_DAO()._getDAO()
    class_name = dao.__class__.__name__
    return class_name == "File" or class_name == "ByWeek"


def get_current_quarter(request):
    """
    Return a restclients.models.sws.Term object
    for the current quarter.
    """
    timer = Timer()
    try:
        comparison_date = get_comparison_date(request)
        term = get_term_by_date(comparison_date)
        after = get_term_after(term)

        if comparison_date > term.grade_submission_deadline.date():
            return after

        return term
    except Exception as ex:
        print ex
        log_exception(logger,
                      'get_current_term',
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      'get_current_term',
                      timer)
    return None


def get_current_summer_term(request):
    """
    Return a string of the current summer a-term or b-term
    """
    term = get_current_quarter(request)
    if get_comparison_date(request) > term.aterm_last_date:
        return "b-term"
    else:
        return "a-term"


def get_next_quarter(request):
    """
    Returna restclients.models.sws.Term object
    for the next quarter.
    """
    timer = Timer()
    try:
        current = get_current_quarter(request)
        return get_term_after(current)
    except Exception as ex:
        log_exception(logger,
                      'get_next_term',
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      'get_next_term',
                      timer)
    return None


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
    return _get_term_by_year_and_quarter(
        get_current_quarter(request).year, 'autumn')


def _get_term_by_year_and_quarter(year, quarter):
    """
    Returns Term object by the given year and quarter.
    If year and quarter are None, return the current term
    """
    logid = ('get_term_by_year_and_quarter ' +
             str(year) + "," + quarter)
    timer = Timer()
    try:
        return sws_term.get_term_by_year_and_quarter(year, quarter)
    except Exception as ex:
        log_exception(logger,
                      logid,
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      logid,
                      timer)
    return None


def get_quarter(year, quarter):
    """
    Returns Term object by the given year and quarter.
    If year and quarter are None, return the current quarter.
    """
    return _get_term_by_year_and_quarter(year, quarter.lower())


def is_past(term, request):
    """
    return true if the term is in the past
    """
    return term.last_final_exam_date < get_comparison_date(request)


def is_a_term(summer_term):
    return summer_term.lower() == "a-term"


def is_b_term(summer_term):
    return summer_term.lower() == "b-term"


def is_half_summer_term(summer_term):
    """
    return True if the given summer_term string is A-term or B-term
    @return True if the given summer_term string is A-term or B-term
    """
    return is_a_term(summer_term) or is_b_term(summer_term)


def is_full_summer_term(summer_term):
    """
    return True if the given summer_term string is Full-term
    @return True if the given summer_term string is Full-term
    """
    return summer_term.lower() == "full-term"


def is_same_summer_term(summer_term1, summer_term2):
    return summer_term1.lower() == summer_term2.lower()


def term_matched(request, given_summer_term):
    """
    @return true if this is not a summer quarter or
    the given_summer_term is overlaped with the current summer term
    """
    current_term = get_current_quarter(request)
    if given_summer_term is None or current_term.quarter != "summer":
        return True
    current_summer_term = get_current_summer_term(request)
    return (is_same_summer_term(current_summer_term, given_summer_term) or
            is_full_summer_term(given_summer_term) and
            is_b_term(current_summer_term))


def is_current_summer_a_term(request):
    """
    @return true if this is in a summer quarter and the A-term
    """
    current_term = get_current_quarter(request)
    return current_term.quarter == "summer" and \
        is_a_term(get_current_summer_term(request))


def get_eof_last_instruction(request, break_at_a_term=False):
    """
    @return the datetime object of the last instruction day for
    current quarter and current summer-term if applicable
    """
    current_term = get_current_quarter(request)
    if break_at_a_term and is_current_summer_a_term(request):
        return convert_to_datetime(current_term.aterm_last_date +
                                   timedelta(days=1))
    else:
        return convert_to_datetime(current_term.last_day_instruction +
                                   timedelta(days=1))


def get_bof_7d_before_last_instruction(request):
    """
    @return the datetime object of the beginning of
    the 7 days before the last instruction day for
    current quarter and current summer-term if applicable.
    Exclude the last instruction day.
    """
    return get_eof_last_instruction(request, True) - timedelta(days=8)


def get_bof_1st_instruction(request):
    """
    @return the datetime object of the begining of quarter start day
    """
    return convert_to_datetime(
        get_current_quarter(request).first_day_quarter)


def get_eof_7d_after_class_start(request):
    """
    @return the datetime object of seven days after the first day for
    current quarter. Exclude the first instruction day.
    """
    return get_bof_1st_instruction(request) + timedelta(days=8)


def get_eof_term(request, break_at_a_term=False):
    """
    @return the datetime object of the end of the grade submission
    deadline or the end of summer a-term if applicable
    """
    current_term = get_current_quarter(request)
    if break_at_a_term and is_current_summer_a_term(request):
        return convert_to_datetime(
            current_term.aterm_last_date +
            timedelta(days=1))
    else:
        return convert_to_datetime(
            current_term.grade_submission_deadline.date() +
            timedelta(days=1))


def get_eof_last_final_exam(request):
    """
    @return the datetime object of the current quarter
    the end of the last final exam day
    """
    return convert_to_datetime(
        get_current_quarter(request).last_final_exam_date +
        timedelta(days=1))


def convert_to_datetime(a_date):
    return datetime(a_date.year, a_date.month, a_date.day,
                    0, 0, 0)
