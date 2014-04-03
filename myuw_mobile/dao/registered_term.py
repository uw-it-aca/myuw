""" 
This module encapsulates the access of the term data
(including registered summer terms, registered future terms).
"""

from datetime import date
import logging
import traceback
from django.conf import settings
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception
from myuw_mobile.dao.term import is_a_term, is_b_term, is_full_summer_term
from myuw_mobile.dao.term import get_current_summer_term
from myuw_mobile.dao.schedule import get_next_quarter_schedule
from myuw_mobile.dao.schedule import get_next_autumn_quarter_schedule
from myuw_mobile.dao.schedule import has_summer_quarter_section


logger =  logging.getLogger(__name__)
FULL_TERM = "F"
A_TERM = "A"
B_TERM = "B"


def _get_registered_summer_terms(registered_summer_sections):
    """
    Return all the summer terms in the registered summer sections
    """
    data = {
        FULL_TERM : False,
        A_TERM : False,
        B_TERM : False,
        }
    for section in registered_summer_sections:
        if is_full_summer_term(section.summer_term):
            data[FULL_TERM] = True
        elif is_a_term(section.summer_term):
            data[A_TERM] = True
        elif is_b_term(section.summer_term):
            data[B_TERM] = True
        else:
            pass
    return data


def _must_displayed_separately (schedule):
    """
    Return True if the summer terms in the schedule sections
    need to be displayed separately
    """
    sumr_tms = _get_registered_summer_terms(schedule.sections)
    return sumr_tms[A_TERM] and sumr_tms[B_TERM] and sumr_tms[FULL_TERM] or sumr_tms[A_TERM] and sumr_tms[FULL_TERM] or sumr_tms[B_TERM] and sumr_tms[FULL_TERM] or sumr_tms[A_TERM] and sumr_tms[B_TERM]
    

def get_current_summer_term_in_schedule (schedule):
    """
    If the summer terms needs to be displayed separately,
    return the current summer term
    """
    summer_term = ""
    if has_summer_quarter_section(schedule) and _must_displayed_separately(schedule):
        summer_term = get_current_summer_term()
    return summer_term


def get_registered_future_quarters():
    """ 
    Return the list of future quarters that 
    has actively enrolled sections
    @param next_quar_sche: ClassSchedule object of a future quarter
    @param next_autumn_quar_sche: 
    """
    terms = []
    next_quar_sche = get_next_quarter_schedule()
    next_quarter = next_quar_sche.term
    if next_quar_sche is not None and len(next_quar_sche.sections) > 0:

        if next_quarter.quarter == "summer":
            if _must_displayed_separately(next_quar_sche):
                sumr_tms = _get_registered_summer_terms(next_quar_sche.sections)

                if sumr_tms[A_TERM]:
                    terms.append(_get_future_term_json(next_quarter,
                                                       "A-Term"))

                if sumr_tms[FULL_TERM] and not sumr_tms[A_TERM]:
                    terms.append(_get_future_term_json(next_quarter,
                                                       "A-Term"))

                if sumr_tms[B_TERM]:
                    terms.append(_get_future_term_json(next_quarter,
                                                       "B-Term"))

                if sumr_tms[FULL_TERM] and not sumr_tms[B_TERM]:
                    terms.append(_get_future_term_json(next_quarter,
                                                       "B-Term"))
            else:
                # summer full-term
                terms.append(_get_future_term_json(next_quarter,""))

            next_autumn_sche = get_next_autumn_quarter_schedule()
            if next_autumn_sche is not None and len(next_autumn_sche.sections) > 0:
                terms.append(_get_future_term_json(next_autumn_sche.term, ""))
        else:
            # non-summer quarter
            terms.append(_get_future_term_json(next_quarter,""))
    return terms


def _get_future_term_json(term, summer_term):
    return_json = term.json_data()
    return_json["summer_term"] = summer_term
    url = "/" + str(term.year) + "," + term.quarter
    if summer_term:
        url = url + "," + summer_term.lower()
    return_json["url"] = url
    return return_json


