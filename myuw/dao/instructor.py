from myuw.models import SeenInstructor
from myuw.dao.term import get_prev_num_terms


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
    for term in get_prev_num_terms(term, 4):
        remove_seen_instructors_for_term(term)

    remove_seen_instructors_for_prior_years(term.year)


def remove_seen_instructors_for_prior_years(year):
    SeenInstructor.objects.filter(year__lte=year).delete()
