""" 
This module encapsulates the access of the term data
(including registered summer terms, registered future terms).
"""

import logging
from myuw_mobile.dao.term import is_a_term, is_b_term, is_full_summer_term
from myuw_mobile.dao.term import get_current_summer_term
from myuw_mobile.dao.schedule import get_next_quarter_schedule
from myuw_mobile.dao.schedule import get_next_autumn_quarter_schedule
from myuw_mobile.dao.schedule import has_summer_quarter_section
from myuw_mobile.dao import get_user_model
from myuw_mobile.models import SeenRegistration
from django.utils import timezone


logger =  logging.getLogger(__name__)
FULL_TERM = "F"
A_TERM = "A"
B_TERM = "B"

FULL_TERM_CREDITS = "FC"
A_TERM_CREDITS = "AC"
B_TERM_CREDITS = "BC"

FULL_TERM_SECTIONS = "FS"
A_TERM_SECTIONS = "AS"
B_TERM_SECTIONS = "BS"

def get_current_summer_term_in_schedule(schedule):
    """
    If the summer terms needs to be displayed separately,
    return the current summer term
    """
    summer_term = ""
    if schedule.term.quarter == 'summer':
        if has_summer_quarter_section(schedule):
            if _must_displayed_separately(schedule):
                summer_term = get_current_summer_term()
            else:
                summer_term = "full-term"
    return summer_term


def get_registered_future_quarters():
    """ 
    Return the list of future quarters that 
    has actively enrolled sections
    """
    next_quar_sche = get_next_quarter_schedule()
    next_autumn_sche = None
    if next_quar_sche and next_quar_sche.term.quarter == 'summer':
        next_autumn_sche = get_next_autumn_quarter_schedule()
    return _get_registered_future_quarters(next_quar_sche,
                                           next_autumn_sche)


def _get_registered_future_quarters(next_quar_sche,
                                    next_autumn_sche):
    """ 
    Return the list of future quarters that 
    has actively enrolled sections

    @param next_quar_sche: ClassSchedule object of a future quarter
    @param next_autumn_quar_sche: ClassSchedule object of the future
           autumn quarter if the next_quar_sche is of summer quarter 
    """
    terms = []
    if next_quar_sche is not None and len(next_quar_sche.sections) > 0:
        next_quarter = next_quar_sche.term

        if next_quarter.quarter == "summer":
            sumr_tms = _get_registered_summer_terms(next_quar_sche.sections)
            
            if sumr_tms[A_TERM] or sumr_tms[FULL_TERM] and sumr_tms[B_TERM]:
                terms.append(_get_future_term_json(next_quarter,
                                                   "a-term",
                                                   sumr_tms))

            if sumr_tms[B_TERM] or sumr_tms[FULL_TERM] and sumr_tms[A_TERM]:
                terms.append(_get_future_term_json(next_quarter,
                                                   "b-term",  
                                                   sumr_tms))

            if sumr_tms[FULL_TERM] and not sumr_tms[A_TERM] and not sumr_tms[B_TERM]:
                terms.append(_get_future_term_json(next_quarter,
                                                   "full-term",
                                                   sumr_tms))
        else:
            terms.append(_get_future_term_json(next_quarter,""))

    if next_autumn_sche is not None and len(next_autumn_sche.sections) > 0:
        terms.append(_get_future_term_json(next_autumn_sche.term, ""))
    return terms


def _get_future_term_json(term, summer_term, summer_term_data=None):
    return_json = term.json_data()
    return_json["summer_term"] = summer_term
    url = "/" + str(term.year) + "," + term.quarter
    if len(summer_term) > 0:
        url = url + "," + summer_term.lower()

        if is_a_term(summer_term):
            return_json["credits"] = str(summer_term_data[FULL_TERM_CREDITS] + summer_term_data[A_TERM_CREDITS])
            return_json["section_count"] = summer_term_data[FULL_TERM_SECTIONS] + summer_term_data[A_TERM_SECTIONS]
        elif is_b_term(summer_term):
            return_json["credits"] = str(summer_term_data[FULL_TERM_CREDITS] + summer_term_data[B_TERM_CREDITS])
            return_json["section_count"] = summer_term_data[FULL_TERM_SECTIONS] + summer_term_data[B_TERM_SECTIONS]
        elif is_full_summer_term(summer_term):
            return_json["credits"] = str(summer_term_data[FULL_TERM_CREDITS])
            return_json["section_count"] = summer_term_data[FULL_TERM_SECTIONS]
    else:
        return_json["credits"] = str(term.credits)
        return_json["section_count"] = term.section_count

    return_json["url"] = url
    return return_json


def _get_registered_summer_terms(registered_summer_sections):
    """
    Return all the summer terms in the registered summer sections
    """
    data = {
        FULL_TERM : False,
        A_TERM : False,
        B_TERM : False,
        FULL_TERM_CREDITS: 0,
        A_TERM_CREDITS: 0,
        B_TERM_CREDITS: 0,
        FULL_TERM_SECTIONS: 0,
        A_TERM_SECTIONS: 0,
        B_TERM_SECTIONS: 0,
        }
    for section in registered_summer_sections:
        if is_full_summer_term(section.summer_term):
            data[FULL_TERM] = True
            data[FULL_TERM_SECTIONS] = data[FULL_TERM_SECTIONS] + 1
            data[FULL_TERM_CREDITS] = data[FULL_TERM_CREDITS] + section.student_credits
        elif is_a_term(section.summer_term):
            data[A_TERM] = True
            data[A_TERM_SECTIONS] = data[A_TERM_SECTIONS] + 1
            data[A_TERM_CREDITS] = data[A_TERM_CREDITS] + section.student_credits
        elif is_b_term(section.summer_term):
            data[B_TERM] = True
            data[B_TERM_SECTIONS] = data[B_TERM_SECTIONS] + 1
            data[B_TERM_CREDITS] = data[B_TERM_CREDITS] + section.student_credits
        else:
            pass
    return data

#MUWM-2210
def should_highlight_future_quarters(schedule):
    should_highlight = False
    now = timezone.now()

    for term in schedule:
        summer_term = "F"
        if term["summer_term"] == "a-term":
            summer_term = "A"
        if term["summer_term"] == "b-term":
            summer_term = "B"

        model, created = SeenRegistration.objects.get_or_create(user=get_user_model(),
                                                                year = term["year"],
                                                                quarter = term["quarter"],
                                                                summer_term = summer_term
                                                                )

        days_diff = (now - model.first_seen_date).days
        if days_diff < 1:
            should_highlight = True

    return should_highlight

def _must_displayed_separately (schedule):
    """
    Return True if the summer terms in the schedule sections
    need to be displayed separately

    Summer terms that must be displayed separately if exist:
    a-term and full-term or 
    b-term and full-term or 
    a-term and b-term

    """
    sumr_tms = _get_registered_summer_terms(schedule.sections)
    return sumr_tms[A_TERM] and sumr_tms[FULL_TERM] or sumr_tms[B_TERM] and sumr_tms[FULL_TERM] or sumr_tms[A_TERM] and sumr_tms[B_TERM]
  

