import logging
from restclients_core.exceptions import DataFailureException
from myuw.models import SeenInstructor
from myuw.dao.instructor_schedule import get_instructor_sections
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

    request.myuw_is_instructor = False
    try:
        person = get_person_of_current_user(request)
        user_netid = person.uwnetid
        if is_seen_instructor(user_netid):
            request.myuw_is_instructor = True
            return True

        term = get_term_before(get_previous_quarter(request))
        sections = get_instructor_sections(person,
                                           term,
                                           future_terms=4,
                                           include_secondaries=False)
        if len(sections) > 0:
            request.myuw_is_instructor = True

            quarter = sections[-1].term.quarter
            year = sections[-1].term.year
            add_seen_instructor(user_netid, year, quarter)
    except DataFailureException as err:
        if err.status != 404:
            raise
    return request.myuw_is_instructor


def is_seen_instructor(uwnetid):
    qset = SeenInstructor.objects.filter(uwnetid=uwnetid)
    return qset.count() > 0


def add_seen_instructor(netid, year, quarter):
    SeenInstructor.objects.update_or_create(uwnetid=netid,
                                            quarter=quarter,
                                            year=year)


def remove_seen_instructors_for_prior_terms(term):
    term_4th_prev = get_prev_num_terms(term, 4)[0]
    remove_seen_instructors_for_prior_years(term_4th_prev.year)


def remove_seen_instructors_for_prior_years(year):
    SeenInstructor.objects.filter(year__lte=year).delete()
