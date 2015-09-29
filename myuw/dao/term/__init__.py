"""
This module direct interfaces with restclient for the term data
"""

from datetime import date, datetime, timedelta
import logging
import traceback
from django.conf import settings
import restclients.sws.term as sws_term
from restclients.dao import SWS_DAO
from restclients.sws.term import get_term_by_date, get_term_after,\
    get_term_before, get_current_term
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time, log_exception


logger = logging.getLogger(__name__)


def convert_date_to_datetime(a_date):
    """
    @return the naive datetime object of the give date object
    """
    return datetime(a_date.year, a_date.month, a_date.day, 0, 0, 0)


def get_comparison_datetime(request):
    """
    Convert the get_comparison_date to a datetime value
    representing 1 second after midnight
    """
    now = get_comparison_date(request)
    return datetime(now.year, now.month, now.day, 0, 0, 1)


def get_comparison_date(request):
    """
    To test at various points in the year, return the date
    overriden if specified in the request;
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


def get_previous_quarter(request):
    """
    Return the Term before the current quarter.
    """
    return get_term_before(get_current_quarter(request))


def get_specific_quarter(year, quarter):
    """
    Returns Term object by the given year and quarter.
    If year and quarter are None, return the current term
    """
    logid = ('get_term_by_year_and_quarter ' + str(year) + "," + quarter)
    timer = Timer()
    try:
        return sws_term.get_term_by_year_and_quarter(year, quarter.lower())
    except Exception as ex:
        log_exception(logger,
                      logid,
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      logid,
                      timer)
    return None


def is_using_file_dao():
    dao = SWS_DAO()._getDAO()
    class_name = dao.__class__.__name__
    return class_name == "File" or class_name == "ByWeek"


def is_past(term, request):
    """
    return true if the term is in the past
    """
    return term.last_final_exam_date < get_comparison_date(request)


def is_a_term(summer_term):
    return summer_term is not None and summer_term.lower() == "a-term"


def is_b_term(summer_term):
    return summer_term is not None and summer_term.lower() == "b-term"


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
