""" 
This module encapsulates the access of the term data
(including registered summer terms, registered future terms).
"""

from datetime import date
import logging
import traceback
from django.conf import settings
import restclients.sws.term as sws_term
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception

logger =  logging.getLogger(__name__)


def get_current_quarter():
    """
    Return a restclients.models.sws.Term object
    for the current quarter.
    """
    timer = Timer()
    try:
        return sws_term.get_current_term()
    except Exception as ex:
        log_exception(logger, 
                      'get_current_term', 
                      traceback.format_exc())
    finally:
        log_resp_time(logger, 
                      'get_current_term',
                      timer)
    return None


def get_current_summer_term():
    """
    Return a string of the current summer a-term or b-term
    """
    term = get_current_quarter()
    if date.today() > term.aterm_last_date:
        return "b-term"
    else:
        return "a-term"


def get_next_quarter():
    """
    Returna restclients.models.sws.Term object
    for the next quarter.
    """
    timer = Timer()
    try:
        return sws_term.get_next_term()
    except Exception as ex:
        log_exception(logger, 
                      'get_next_term', 
                      traceback.format_exc())
    finally:
        log_resp_time(logger, 
                      'get_next_term',
                      timer)
    return None


def get_next_non_summer_quarter():
    term = get_next_quarter()
    if term.quarter == "summer":
        return get_next_autumn_quarter()

    return term


def get_next_autumn_quarter():
    """
    Return the Term object for the next autumn quarter in the same year
    when in the Spring quarter
    """
    return _get_term_by_year_and_quarter(
        get_current_quarter().year, 'autumn')


def _get_term_by_year_and_quarter(year, quarter):
    """
    Returns Term object by the given year and quarter.
    If year and quarter are None, return the current term
    """
    logid = ('get_term_by_year_and_quarter ' + 
             str(year) + "," + quarter);
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


def get_quarter(year=None, quarter=None):
    """
    Returns Term object by the given year and quarter.
    If year and quarter are None, return the current quarter.
    """
    if year and quarter:
        return _get_term_by_year_and_quarter(year, quarter.lower())
    else:
        return get_current_quarter()


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


def is_past(term):
    """
    return true if the term is in the past
    """
    return term.last_final_exam_date < date.today()


