# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from datetime import date
from django.core.management.base import BaseCommand
from uw_pws import PWS
from uw_sws.section import get_last_section_by_instructor_and_terms
from uw_sws.term import get_specific_term
from myuw.dao import is_using_file_dao
from myuw.models import Instructor

logger = logging.getLogger(__name__)
pws = PWS()


class Command(BaseCommand):
    # clean up or update the old instructor records.
    # run once in early autumn quarter of each year

    def handle(self, *args, **options):
        cur_year = date.today().year
        start_year = cur_year - 6  # keep those within 6 years

        if is_using_file_dao():
            # mock data
            term = get_specific_term(2012, 'autumn')
            number_of_future_terms = 4
        else:
            term = get_specific_term(start_year, 'autumn')
            number_of_future_terms = 25
        deleted = 0
        updated = 0
        records = Instructor.objects.filter(year__lt=start_year)
        logger.info("Total records prior of {}: {}".format(
            start_year, len(records)))
        for rec in records:
            person = pws.get_person_by_netid(rec.user.uwnetid)
            # check if the user has taught any course since then
            sectionref = get_last_section_by_instructor_and_terms(
                person, term, number_of_future_terms,
                transcriptable_course='all',
                delete_flag=['active', 'suspended'])

            if sectionref:
                # update the record
                quarter = sectionref.term.quarter
                year = sectionref.term.year
                try:
                    # to avoid UNIQUE constraint err
                    Instructor.objects.filter(user=rec.user).delete()
                    Instructor.objects.update_or_create(
                        user=rec.user, year=year, quarter=quarter)
                    updated += 1
                except Exception as ex:
                    logger.error("update({}, {}, {}): {}".format(
                        person.uwnetid, year, quarter, ex))
            else:
                try:
                    rec.delete()
                    deleted += 1
                except Exception as ex:
                    logger.error("delete({}): {}".format(
                        rec.user.uwnetid, ex))

        logger.info(
            "Deleted {} records. Updated {} records".format(deleted, updated))
