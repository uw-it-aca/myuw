import logging
from myuw.models import Instructor
from uw_sws.section import get_last_section_by_instructor_and_terms
from myuw.dao import is_using_file_dao
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.term import get_term_before, get_previous_quarter,\
    get_current_quarter
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
    sectionref = get_most_recent_sectionref_by_instructor(request)
    if sectionref:
        request.myuw_is_instructor = True
        set_instructor(user, sectionref)
    return request.myuw_is_instructor


def get_most_recent_sectionref_by_instructor(request):
    if is_using_file_dao():
        term = get_term_before(get_previous_quarter(request))
        future_term = 4
    else:
        cur_term = get_current_quarter(request)
        term = get_specific_term(cur_term.year - 6, cur_term.quarter)
        if cur_term.quarter == 'spring':
            future_term = 26
        else:
            future_term = 25

    person = get_person_of_current_user(request)
    return get_last_section_by_instructor_and_terms(
        person, term, future_term,
        transcriptable_course='all',
        delete_flag=['active', 'suspended'])


def set_instructor(user, sectionref):
    quarter = sectionref.term.quarter
    year = sectionref.term.year
    try:
        Instructor.add_seen_instructor(user, year, quarter)
    except Exception as ex:
        logger.error("add_seen_instructor(%s, %s, %s) ==> %s",
                     user.uwnetid, year, quarter, ex)
