# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Clean up the entries no longer useful
"""

import logging
import time
from datetime import timedelta
from django.core.mail import send_mail
from django.db import connection
from django.core.management.base import BaseCommand, CommandError
from uw_sws import sws_now, SWS_TIMEZONE
from myuw.models import (
    VisitedLinkNew, SeenRegistration, UserNotices, UserCourseDisplay)
from myuw.dao.term import get_term_by_date, get_term_before
from myuw.util.settings import get_cronjob_recipient, get_cronjob_sender
from myuw.logger.timer import Timer

logger = logging.getLogger(__name__)
batch_size = 1000


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('name', choices=[
            'course', 'notice', 'seenreg', 'linkvisit', 'noop'],
            help="The table to check ")

    def handle(self, *args, **options):
        self.action = options['name']
        self.error = ""
        if self.action == 'noop':
            return
        if self.action == 'course':
            self.course_display()
        if self.action == 'notice':
            self.notice_read()
        if self.action == 'seenreg':
            self.registration_seen()
        if self.action == 'linkvisit':
            self.link_visited()

        if len(self.error):
            send_mail(self.error,
                      "{}@uw.edu".format(get_cronjob_sender()),
                      ["{}@uw.edu".format(get_cronjob_recipient())])

    def get_cut_off_date(self, days_delta=364):
        # default is 52 weeks (364 days)
        now = SWS_TIMEZONE.localize(sws_now())
        return now - timedelta(days=days_delta)

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
            self.error = "{} {}\n".format(queryf, ex)
            logger.error(self.error)
            raise CommandError(self.error)

    def course_display(self):
        # clean up after one year
        timer = Timer()
        queryf = "DELETE FROM user_course_display_pref WHERE id IN ({})"
        term = get_term_by_date(sws_now())
        y = term.year - 1
        q = term.quarter
        qset = UserCourseDisplay.objects.filter(year=y, quarter=q)
        if qset.exists():
            ids_to_delete = qset.values_list('id', flat=True)
            self.deletion(ids_to_delete, queryf)
            logger.info(
                "Delete UserCourseDisplay {} {}, Time: {} sec\n".format(
                    y, q, timer.get_elapsed()))

    def notice_read(self):
        # clean up after 180 days
        timer = Timer()
        queryf = "DELETE FROM myuw_mobile_usernotices WHERE id IN ({})"
        cut_off_dt = self.get_cut_off_date(180)
        qset = UserNotices.objects.filter(first_viewed__lt=cut_off_dt)
        if qset.exists():
            ids_to_delete = qset.values_list('id', flat=True)
            self.deletion(ids_to_delete, queryf)
            logger.info(
                "Delete UserNotices viewed before {} Time: {} sec\n".format(
                    cut_off_dt, timer.get_elapsed()))

    def registration_seen(self):
        # clean up previous quarters'
        timer = Timer()
        queryf = "DELETE FROM myuw_mobile_seenregistration WHERE id IN ({})"
        term = get_term_before(get_term_by_date(sws_now()))
        qset = SeenRegistration.objects.filter(
            year=term.year, quarter=term.quarter)
        if qset.exists():
            ids_to_delete = qset.values_list('id', flat=True)
            self.deletion(ids_to_delete, queryf)
            logger.info(
                "Delete SeenRegistration {} {} Time: {}\n".format(
                    term.year, term.quarter, timer.get_elapsed()))

    def link_visited(self):
        # clean up after one year
        timer = Timer()
        queryf = "DELETE FROM myuw_visitedlinknew WHERE id IN ({})"
        cut_off_dt = self.get_cut_off_date()
        qset = VisitedLinkNew.objects.filter(visit_date__lt=cut_off_dt)
        if qset.exists():
            ids_to_delete = qset.values_list('id', flat=True)
            self.deletion(ids_to_delete, queryf)
            logger.info(
                "Delete VisitedLinkNew viewed before {} Time: {}\n".format(
                    cut_off_dt, timer.get_elapsed()))
