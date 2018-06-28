import logging
from myuw.models import Instructor
from uw_sws.section import get_last_section_by_instructor_and_terms
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.term import get_term_before, get_previous_quarter
from myuw.dao.user import get_user_model

logger = logging.getLogger(__name__)


def is_instructor_prefetch():
    def _method(request):
        is_instructor(request)
    return [_method]


def is_instructor(request):
    """
    Determines if user is an instructor of the request's term
    """
    if hasattr(request, "myuw_is_instructor"):
        return request.myuw_is_instructor

    user = get_user_model(request)
    if Instructor.is_seen_instructor(user):
        request.myuw_is_instructor = True
        return True

    request.myuw_is_instructor = False
    term = get_term_before(get_previous_quarter(request))
    person = get_person_of_current_user(request)
    section = get_last_section_by_instructor_and_terms(
        person, term, 4, transcriptable_course='all',
        delete_flag=['active', 'suspended'])

    if section:
        request.myuw_is_instructor = True
        set_instructor(user, section)
    return request.myuw_is_instructor


def set_instructor(user, section):
    quarter = section.term.quarter
    year = section.term.year
    try:
        Instructor.add_seen_instructor(user, year, quarter)
    except Exception as ex:
        logger.error("add_seen_instructor(%s, %s, %s) ==> %s",
                     user.uwnetid, year, quarter, ex)
