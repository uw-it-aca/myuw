from myuw.models import SeenInstructor
from uw_sws.term import get_term_before


def is_seen_instructor(uwnetid):
    qset = SeenInstructor.objects.filter(uwnetid=uwnetid)
    return qset.count() > 0


def add_seen_instructor(uwnetid, term):
    SeenInstructor.objects.update_or_create(
        uwnetid=uwnetid, year=term.year, quarter=term.quarter)


def remove_seen_instructors_for_term(term):
    SeenInstructor.objects.filter(
        year=term.year,
        quarter=term.quarter
    ).delete()


def remove_seen_instructors_for_prior_terms(term):
    # prune anything beyond prior terms
    for i in range(4):
        term = get_term_before(term)
        remove_seen_instructors_for_term(term)

    remove_seen_instructors_for_prior_years(term.year)


def remove_seen_instructors_for_prior_years(year):
    SeenInstructor.objects.filter(year__lte=year).delete()
