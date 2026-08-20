# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Clean up the entries no longer useful
"""

import logging
import time
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from myuw.dao.term import (
    get_term_after,
    get_term_before,
    get_term_by_date,
    tz_aware_now,
    tz_naive_now,
)
from myuw.logger.timer import Timer
from myuw.models import SeenRegistration, UserCourseDisplay, UserNotices, VisitedLinkNew

logger = logging.getLogger(__name__)
batch_size = 1000


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('name', choices=[
            'course', 'notice', 'seenreg', 'linkvisit'],
            help="The table to check ")

    def handle(self, *args, **options):
        self.action = options['name']

        if self.action == 'course':
            self.course_display()
        if self.action == 'notice':
            self.notice_read()
        if self.action == 'seenreg':
            self.registration_seen()
        if self.action == 'linkvisit':
            self.link_visited()

    def get_cut_off_date(self, days_delta=180):
        # default is 180 days
        return tz_aware_now() - timedelta(days=days_delta)

    def deletion(self, ids_to_delete, queryf):
        try:
            while ids_to_delete and len(ids_to_delete) > 0:
                batch_ids = ids_to_delete[:batch_size]
                with connection.cursor() as cursor:
                    placeholders = ','.join(
                        str(id) for id in batch_ids)
                    cursor.execute(
                        queryf.format(placeholders))
                time.sleep(2)
                ids_to_delete = ids_to_delete[batch_size:]
        except Exception as ex:
            logger.error(f"{queryf} {ex}\n")
            raise CommandError(f"{queryf} {ex}")

    def get_cur_term(self):
        comparison_date = tz_naive_now().date()
        term = get_term_by_date(comparison_date)
        # Match MyUW quarter switchS
        if comparison_date > term.grade_submission_deadline.date():
            return get_term_after(term)
        return term

    def course_display(self):
        # clean up after one year
        timer = Timer()
        queryf = "DELETE FROM user_course_display_pref WHERE id IN ({})"
        term = self.get_cur_term()
        y = term.year - 1
        q = term.quarter
        qset = UserCourseDisplay.objects.filter(year=y, quarter=q)
        if qset.exists():
            ids_to_delete = qset.values_list('id', flat=True)
            self.deletion(ids_to_delete, queryf)
            logger.info(
                f"Delete UserCourseDisplay {y} {q}, Time: {timer.get_elapsed()} sec\n")
        else:
            logger.info("Found no entry to delete")

        count = UserCourseDisplay.objects.all().count()
        logger.info(f"UserCourseDisplay has {count} entries")

    def notice_read(self):
        # clean up after 180 days
        timer = Timer()
        queryf = "DELETE FROM myuw_mobile_usernotices WHERE id IN ({})"
        cut_off_dt = self.get_cut_off_date()
        qset = UserNotices.objects.filter(first_viewed__lt=cut_off_dt)
        if qset.exists():
            ids_to_delete = qset.values_list('id', flat=True)
            self.deletion(ids_to_delete, queryf)
            logger.info(
                f"Delete UserNotices viewed before {cut_off_dt} "
                f"Time: {timer.get_elapsed()} sec\n")
        else:
            logger.info("Found no entry to delete")

        count = UserNotices.objects.all().count()
        logger.info(f"UserNotices has {count} entries")

    def registration_seen(self):
        # clean up previous quarters'
        timer = Timer()
        queryf = "DELETE FROM myuw_mobile_seenregistration WHERE id IN ({})"
        term = get_term_before(self.get_cur_term())
        qset = SeenRegistration.objects.filter(
            year=term.year, quarter=term.quarter)
        if qset.exists():
            ids_to_delete = qset.values_list('id', flat=True)
            self.deletion(ids_to_delete, queryf)
            logger.info(
                f"Delete SeenRegistration {term.year} {term.quarter} "
                f"Time: {timer.get_elapsed()}\n")
        else:
            logger.info("Found no entry to delete")

        count = SeenRegistration.objects.all().count()
        logger.info(f"SeenRegistration has {count} entries")

    def link_visited(self):
        # clean up after 180 days
        timer = Timer()
        queryf = "DELETE FROM myuw_visitedlinknew WHERE id IN ({})"
        cut_off_dt = self.get_cut_off_date()
        qset = VisitedLinkNew.objects.filter(visit_date__lt=cut_off_dt)
        if qset.exists():
            ids_to_delete = qset.values_list('id', flat=True)
            self.deletion(ids_to_delete, queryf)
            logger.info(
                f"Delete VisitedLinkNew viewed before {cut_off_dt} "
                f"Time: { timer.get_elapsed()}\n")
        else:
            logger.info("Found no entry to delete")

        count = VisitedLinkNew.objects.all().count()
        logger.info(f"VisitedLinkNew has {count} entries")
