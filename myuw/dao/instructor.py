import logging
from restclients_core.exceptions import DataFailureException
from myuw.models import SeenInstructor
from uw_sws.section import get_last_section_by_instructor_and_terms
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.term import get_prev_num_terms,\
    get_term_before, get_previous_quarter

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

    person = get_person_of_current_user(request)
    user_netid = person.uwnetid
    if is_seen_instructor(user_netid):
        request.myuw_is_instructor = True
        return True

    request.myuw_is_instructor = False
    term = get_term_before(get_previous_quarter(request))
    section = get_last_section_by_instructor_and_terms(
        person, term, 4, transcriptable_course='all',
        delete_flag=['active', 'suspended'])

    if section:
        request.myuw_is_instructor = True
        quarter = section.term.quarter
        year = section.term.year
        try:
            add_seen_instructor(user_netid, year, quarter)
        except Exception as ex:
            logger.error("add_seen_instructor(%s, %s, %s) ==> %s",
                         user_netid, year, quarter, ex)
    return request.myuw_is_instructor


def is_seen_instructor(uwnetid):
    return SeenInstructor.objects.filter(uwnetid=uwnetid).exists()


def add_seen_instructor(netid, year, quarter):
    SeenInstructor.objects.update_or_create(uwnetid=netid,
                                            quarter=quarter,
                                            year=year)


def remove_seen_instructors_yrs_before(year):
    SeenInstructor.objects.filter(year__lt=year).delete()
