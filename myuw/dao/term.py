"""
This module direct interfaces with restclient for the term data
"""

from datetime import date, datetime, timedelta
import logging
import pytz
from django.conf import settings
from django.utils import timezone
from uw_sws.models import Term
from restclients.util.datetime_convertor import convert_to_begin_of_day, \
    convert_to_end_of_day
from uw_sws.section import is_a_term, is_b_term, is_full_summer_term
from uw_sws.term import get_term_by_date, get_specific_term, \
    get_current_term, get_next_term, get_previous_term, \
    get_term_before, get_term_after, get_next_autumn_term, \
    get_next_non_summer_term
from myuw.dao import is_using_file_dao


logger = logging.getLogger(__name__)


def get_default_date():
    """
    A hook to help with mock data testing - put the default date
    right in the middle of the "current" term.
    """
    return get_default_datetime().date()


def get_default_datetime():
    """
    A hook to help with mock data testing - put the default datetime
    right in the middle of the "current" term.
    """
    if is_using_file_dao():
        term = get_current_term()
        first_day = term.first_day_quarter
        default_date = first_day + timedelta(days=14)
        return datetime(default_date.year,
                        default_date.month,
                        default_date.day,
                        0, 0, 1)
    return datetime.now()


def get_comparison_datetime(request):
    """
    To test at various points in the year, return the datetime
    overriden if specified in the request;
    otherwise return the default datetime. Format: YYYY-MM-DDTHH:MM:SS
    """
    FORMAT = "%Y-%m-%d %H:%M:%S"

    override_date = None
    if request:
        if "myuw_override_date" in request.session:
            try:
                val = request.session["myuw_override_date"]
                override_date = datetime.strptime(val, FORMAT)
            except ValueError:
                # Accepts an override date as well, but adds 1 second
                # so date logic works
                try:
                    date_format = "%Y-%m-%d"
                    override_date = datetime.strptime(val, date_format) + \
                        timedelta(seconds=1)
                except Exception:
                    raise
            except Exception as ex:
                pass

    if override_date:
        return override_date

    return get_default_datetime()


def get_comparison_date(request):
    """
    Convert the get_comparison_datetime to a date value
    """
    now = get_comparison_datetime(request)
    return now.date()


def get_comparison_datetime_with_tz(request):
    """
    @return the local timezone awared datetime object
    """
    local_tz = timezone.get_current_timezone()
    return local_tz.localize(
        get_comparison_datetime(request)).astimezone(pytz.utc)


def get_current_quarter(request):
    """
    Return a uw_sws.models.Term object
    for the current quarter refered in the user session.
    """
    if hasattr(request, 'myuw_current_quarter'):
        return request.myuw_current_quarter

    comparison_date = get_comparison_date(request)
    term = get_term_by_date(comparison_date)
    after = get_term_after(term)

    if comparison_date > term.grade_submission_deadline.date():
        request.myuw_current_quarter = after
        return after

    request.myuw_current_quarter = term
    return term


def get_next_quarter(request):
    """
    Returns a uw_sws.models.Term object
    for the current quarter refered in the user session.
    """
    if hasattr(request, 'myuw_next_quarter'):
        return request.myuw_next_quarter
    term = get_term_after(get_current_quarter(request))
    request.myuw_next_quarter = term
    return term


def get_current_and_next_quarters(request, num):
    """
    Returns the current and next num uw_sws.models.Term objects in a list
    for the current quarter refered in the user session. Returns the next
    num -1 quarters
    """
    if hasattr(request, 'myuw_next_quarter'):
        return request.myuw_next_quarter
    term = get_current_quarter(request)
    quarters = [term]

    for x in range(1, num):
        term = get_term_after(term)
        quarters.append(term)

    return quarters


def get_previous_quarter(request):
    """
    for the current quarter refered in the user session.
    """
    if hasattr(request, "myuw_previous_quarter"):
        return request.myuw_previous_quarter
    term = get_term_before(get_current_quarter(request))
    request.myuw_previous_quarter = term
    return term


def is_past(term, request):
    """
    return true if the given term is in the past
    """
    return term.get_eod_last_final_exam() < get_comparison_datetime(request)


def is_future(term, request):
    """
    return true if the given term is in the future
    """
    return term.get_bod_first_day() > get_comparison_datetime(request)


def is_in_summer_quarter(request):
    """
    Return True if the user session is currently in a summer quarter
    """
    return get_current_quarter(request).is_summer_quarter()


def get_current_summer_term(request):
    """
    Return a string of the current summer a-term or b-term
    or None if it is not a summer quarter
    """
    if not is_in_summer_quarter(request):
        return None
    eod_aterm = get_current_quarter(request).get_eod_summer_aterm()
    if get_comparison_datetime(request) > eod_aterm:
        return "b-term"
    else:
        return "a-term"


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


def get_next_non_summer_quarter(request):
    """
    Return the Term object for the non-summer quarter after the quarter
    refered in the current user sesssion.
    """
    return get_next_non_summer_term(get_current_quarter(request))


def get_next_autumn_quarter(request):
    """
    Return the Term object for the next autumn quarter in the same year.
    """
    return get_next_autumn_term(get_current_quarter(request))


def get_eod_current_summer_aterm(request):
    """
    @return the datetime object of the end of day for the current
    summer quarter A-term (it is also the beginning of summer B-term).
    If it is currently not a summer term, return None.
    """
    if is_in_summer_a_term(request):
        return get_current_quarter(request).get_eod_summer_aterm()
    return None


def _get_correspond_eod(the_day, request, break_at_a_term):
    """
    @return the datetime object of the end of given "fn" day
    for current quarter and the end of the current summer A-term if applicable.
    """
    eof_aterm_last_day = get_eod_current_summer_aterm(request)
    if break_at_a_term and eof_aterm_last_day is not None:
        return eof_aterm_last_day
    return the_day


def get_bod_current_term_class_start(request, break_at_a_term=False):
    """
    @return the datetime object of the begining of quarter start day
    or the beginning of summer B-term if applicable
    """
    return _get_correspond_eod(
            get_current_quarter(request).get_bod_first_day(),
            request, break_at_a_term)


def get_eod_7d_after_class_start(request, break_at_a_term=False):
    """
    @return the datetime object of seven days after the first day for
    current quarter. Exclude the first instruction day.
    """
    return (get_bod_current_term_class_start(request, break_at_a_term) +
            timedelta(days=8))


def get_bod_class_start_quarter_after(term):
    """
    Return the datetime object of the beginning of the first instruction
    day in the term after the give year and quarter.
    Only the summer full term is relevant.
    """
    nterm = get_term_after(term)
    if nterm is None:
        return None
    return nterm.get_bod_first_day()


def get_eod_current_term(request, break_at_a_term=False):
    """
    @return the datetime object of the end of the grade submission
    deadline or the end of summer a-term if applicable
    """
    return _get_correspond_eod(
            get_current_quarter(request).get_eod_grade_submission(),
            request, break_at_a_term)


def get_eod_current_term_last_instruction(request, break_at_a_term=False):
    """
    @return the datetime object of the end of the last instruction day
    for current quarter and current summer A-term if applicable
    """
    return _get_correspond_eod(
            get_current_quarter(request).get_eod_last_instruction(),
            request, break_at_a_term)


def get_bod_7d_before_last_instruction(request):
    """
    @return the datetime object of the beginning of
    the 7 days before the last instruction day for
    current quarter and current summer-term if applicable.
    Exclude the last instruction day.
    """
    return (get_eod_current_term_last_instruction(request, True) -
            timedelta(days=8))


def get_eod_current_term_last_final_exam(request, break_at_a_term=False):
    """
    @return the datetime object of the current quarter
    the end of the last final exam day
    """
    return _get_correspond_eod(
        get_current_quarter(request).get_eod_last_final_exam(),
        request, break_at_a_term)


def get_eod_specific_quarter(year, quarter):
    """
    Return the datetime object of the end of day on grade submission deadline
    for the term of the give year and quarter.
    Only the summer full term is relevant.
    """
    return get_specific_term(year, quarter).get_eod_grade_submission()


def get_eod_specific_quarter_after(year, quarter):
    """
    Return the datetime object of the end of day on grade submission deadline
    for the term after the give year and quarter.
    Only the summer full term is relevant.
    """
    return get_term_after(
            get_specific_term(year, quarter)).get_eod_grade_submission()


def get_eod_specific_quarter_last_instruction(year, quarter):
    """
    Return the datetime object of the end of last instruction
    for the term of the give year and quarter.
    Only the summer full term is relevant.
    """
    return get_specific_term(year, quarter).get_eod_last_instruction()


# The affilliation method caches values on the request object, but this one
# is just designed to get values into our caching system.
def _get_term_method(year, quarter):
    def generated(request):
        get_specific_term(year, quarter)
    return generated


def current_terms_prefetch(request):
    # This triggers a call to get_current_term when using the file dao.
    # That request won't happen on test/production
    compare = get_comparison_date(request)
    year = compare.year
    month = compare.year

    methods = []

    for quarter in ('autumn', 'summer', 'spring', 'winter'):
        methods.append(_get_term_method(year, quarter))

    if month < 4:
        methods.append(_get_term_method(year-1, 'autumn'))

    if month > 6:
        methods.append(_get_term_method(year+1, 'winter'))

    if month > 9:
        methods.append(_get_term_method(year+1, 'spring'))

    return methods
