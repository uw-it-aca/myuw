"""
This module direct interfaces with restclient for the term data
"""

from datetime import date, datetime, timedelta
import logging
from django.utils import timezone
from uw_sws.models import Term
from uw_sws.util import convert_to_begin_of_day, convert_to_end_of_day
from uw_sws.section import is_a_term, is_b_term, is_full_summer_term
from uw_sws.term import get_term_by_date, get_specific_term, \
    get_current_term, get_next_term, get_previous_term, \
    get_term_before, get_term_after, get_next_autumn_term, \
    get_next_non_summer_term
from restclients_core.exceptions import DataFailureException
from myuw.dao import is_using_file_dao, sws_now


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
    return timezone.make_aware(get_comparison_datetime(request))


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


def get_term_from_quarter_string(quarter_string):
    """
    Return a uw_sws.models.Term object
    for the current quarter string passed in.
    """
    term_identifiers = quarter_string.split(",")
    year = term_identifiers[0]
    quarter = term_identifiers[1]

    return get_specific_term(year, quarter)


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
    num -1 quarters along with the current one.
    """
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


def get_previous_number_quarters(request, num):
    """
    for previous quarters prior to current quarter
    refered in the user session.
    """
    term = get_current_quarter(request)
    return get_prev_num_terms(term, num)


def get_future_number_quarters(request, num):
    """
    for future quarters prior to current quarter
    refered in the user session.
    """
    term = get_current_quarter(request)
    return get_future_num_terms(term, num)


def get_prev_num_terms(term, num):
    """
    return num prior term objects in ascending order
    """
    terms = []
    for i in range(num):
        try:
            term = get_term_before(term)
            terms.insert(0, term)
        except DataFailureException as ex:
            if ex.status == 404:
                pass

    return terms


def get_future_num_terms(term, num):
    """
    return num future term objects in ascending order
    """
    terms = []
    for i in range(num):
        try:
            term = get_term_after(term)
            terms.append(term)
        except DataFailureException as ex:
            if ex.status == 404:
                pass

    return terms


def is_past(term, request):
    """
    return true if the given term is in the past
    """
    return term.is_past(get_comparison_datetime(request))


def is_future(term, request):
    """
    return true if the given term is in the future
    """
    return term.is_future(get_comparison_datetime(request))


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


def add_term_data_to_context(request, context):
    """
    Updates a dictionary with information about what's happening now.

    Includes the data, the quarter (or break), and the week of the quarter.
    """
    terms = get_current_and_next_quarters(request, 2)
    cur_term = terms[0]
    next_term = terms[1]

    if cur_term is None:
        context["err"] = "No current quarter data!"
        return

    compare = get_comparison_date(request)
    context['today'] = compare
    context['is_break'] = False
    if compare < cur_term.first_day_quarter:
        context['is_break'] = True

    break_term = cur_term
    if compare > cur_term.last_final_exam_date:
        context['is_break'] = True
        break_term = get_term_after(cur_term)

    context["year"] = cur_term.year
    context["quarter"] = cur_term.quarter.lower()

    if "display_term" not in context:
        context["display_term"] = {
            "year": context["year"],
            "quarter": context["quarter"]
            }

    context["break_year"] = break_term.year
    context["break_quarter"] = break_term.quarter

    context['is_finals'] = False
    if (compare > cur_term.last_day_instruction and
            compare <= cur_term.last_final_exam_date):
        context['is_finals'] = True

    context['first_day'] = cur_term.first_day_quarter
    context['last_day'] = cur_term.last_day_instruction
    context["first_day_quarter"] = cur_term.first_day_quarter
    context["last_day_instruction"] = cur_term.last_day_instruction
    context["aterm_last_date"] = cur_term.aterm_last_date
    context["bterm_first_date"] = cur_term.bterm_first_date

    context["next_year"] = next_term.year
    context["next_quarter"] = next_term.quarter


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
