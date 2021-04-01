# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from uw_sws.section import get_changed_sections_by_term, get_section_by_url
from uw_sws.term import get_current_term
from myuw.dao.instructor import add_seen_instructor,\
    remove_seen_instructors_for_prior_terms
from myuw.dao.instructor_schedule import get_prior_instructed_terms


class Command(BaseCommand):
    help = "Add instructors from past quarters to the SeenInstructor table"

    def handle(self, *args, **options):
        change_since = '2010-07-07'
        prior_terms = get_prior_instructed_terms(get_current_term())
        for term in prior_terms:
            for section_ref in get_changed_sections_by_term(
                    change_since, term):
                section = get_section_by_url(section_ref.url)
                for instructor in section.get_instructors():
                    add_seen_instructor(instructor.uwnetid, term)

        remove_seen_instructors_for_prior_terms(prior_terms[0])
