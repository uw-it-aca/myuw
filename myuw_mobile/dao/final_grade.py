"""
This module provides final grades in the SWS Enrollment resource
"""

import logging
import traceback
from restclients.models import ClassSchedule
from restclients.sws.enrollment import get_grades_by_regid_and_term
from myuw_mobile.dao.pws import get_regid_of_current_user
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception


logger =  logging.getLogger(__name__)


def get_grades_by_term(term):
    """ 
    @return a dictionary of section label and 
    restclients.models.sws.StudentGrades object
    Returns a final grades indexed by section label
    for the current user in the given term/quarter 
    """
    regid = get_regid_of_current_user()
    if regid is None or term is None:
        return None
    logid = ('get_grades_by_regid_and_term ' + 
             str(regid) + ',' + str(term.year) + ',' + term.quarter)
    timer = Timer()
    try:
        return _grades_indexed_by_section_label(
            get_grades_by_regid_and_term(regid, term))
    except Exception as ex:
        log_exception(logger,
                      logid,
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      logid,
                      timer)
    return None


def _grades_indexed_by_section_label(final_grades):
    grade_by_section_label = {}
    for grade in final_grades.grades:
        grade_by_section_label[grade.section.section_label()] = grade
    return grade_by_section_label
