from django.core.management.base import BaseCommand
from uw_sws.section import get_changed_sections_by_term, get_section_by_url
from uw_sws.term import get_current_term, get_term_before
from myuw.models import User, SeenInstructor
from myuw.dao.instructor_schedule import get_prior_instructed_terms


class Command(BaseCommand):
    help = "Add instructors from past quarters to the SeenInstructor table"

    def handle(self, *args, **options):
        change_since = '2010-07-07'
        prior_terms = get_prior_instructed_terms(get_current_term())
        for term in prior_terms:
            print "TERM: %s-%s" % (term.year, term.quarter)
            for section_ref in get_changed_sections_by_term(
                    change_since, term):
                print "section_ref.url: %s" % (section_ref.url)
                section = get_section_by_url(section_ref.url)
                for instructor in section.get_instructors():
                    print "instructor: %s" % (instructor.uwnetid)
                    user, created = User.objects.get_or_create(
                        uwnetid=instructor.uwnetid,
                        uwregid=instructor.uwregid)
                    seen, created = SeenInstructor.objects.update_or_create(
                        user=user,
                        year=term.year,
                        quarter=term.quarter)

        # prune anything beyond prior terms
        term = prior_terms[0]
        for i in range(4):
            term = get_term_before(term)
            SeenInstructor.objects.filter(
                year=term.year,
                quarter=term.quarter
            ).delete()

        SeenInstructor.objects.filter(year__lte=term.year).delete()
