# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Clean up the entries no longer useful
"""

import logging
import time
from datetime import timedelta
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sessions.models import Session
from django.utils import timezone
from uw_sws import sws_now
from myuw.models import (
    VisitedLinkNew, SeenRegistration,
    UserNotices, UserCourseDisplay)
from myuw.dao.term import get_term_by_date, get_term_before
from myuw.util.settings import get_cronjob_recipient, get_cronjob_sender
from myuw.logger.timer import Timer

logger = logging.getLogger(__name__)
batch_size = 1000


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('name', choices=[
            'course', 'notice', 'seenreg', 'linkvisit'],
            help="The table to check ")

    def handle(self, *args, **options):
        self.errors = []
        self.action = options['name']

        if self.action == 'course':
            self.course_display()
        if self.action == 'notice':
            self.notice_read()
        if self.action == 'seenreg':
            self.registration_seen()
        if self.action == 'linkvisit':
            self.link_visited()

        if len(self.errors):
            send_mail("Clear Expired Django Session Weekly Cron",
                      "\n".join(self.errors),
                      "{}@uw.edu".format(get_cronjob_sender()),
                      ["{}@uw.edu".format(get_cronjob_recipient())])

    def get_cut_off_date(self, days_delta=364):
        # default is 52 weeks (364 days)
        now = sws_now().date()
        return now - timedelta(days=days_delta)

    def course_display(self):
        # clean up after one year
        timer = Timer()
        for y in range(2000, 2022):
            for q in ["winter", "spring", "summer", "autumn"]:
                for c in range(1, 9):
                    entries_to_delete = UserCourseDisplay.objects.filter(
                        year=y, quarter=q, color_id=c)
                    if not entries_to_delete.exists():
                        continue
                    while entries_to_delete.exists():
                        try:
                            batch = entries_to_delete[:batch_size]
                            batch.delete()
                            time.sleep(1)
                            entries_to_delete = entries_to_delete[batch_size:]
                        except Exception as ex:
                            logger.error(
                                "{} Delete Batch {}:{}:{} {}\n".format(
                                    "UserCourseDisplay", y, q, c, ex))
                            raise CommandError(ex)
                logger.info(
                    "UserCourseDisplay delete {} {} Time: {} seconds\n".format(
                        y, q, timer.get_elapsed()
                    ))

    def notice_read(self):
        # clean up after 180 days
        timer = Timer()
        cut_off_dt = self.get_cut_off_date(180)
        entries_to_delete = UserNotices.objects.filter(
            first_viewed__lt=cut_off_dt)
        while entries_to_delete.exists():
            try:
                batch = entries_to_delete[:batch_size]
                batch.delete()
                time.sleep(1)
                entries_to_delete = entries_to_delete[batch_size:]
            except Exception as ex:
                logger.error("UserNotices delete {}\n".format(ex))
                raise CommandError(ex)
        logger.info("UserNotices Delete viewed before {} Time: {}\n".format(
                    cut_off_dt, timer.get_elapsed()))

    def registration_seen(self):
        # clean up after the quarter ends
        timer = Timer()
        for y in range(2013, 2023):
            for q in ["winter", "spring", "summer", "autumn"]:
                entries_to_delete = SeenRegistration.objects.filter(
                    year=y, quarter=q)
                if not entries_to_delete.exists():
                    continue
                while entries_to_delete.exists():
                    try:
                        batch = entries_to_delete[:batch_size]
                        batch.delete()
                        time.sleep(1)
                        entries_to_delete = entries_to_delete[batch_size:]
                    except Exception as ex:
                        logger.error("SeenRegistration delete {}\n".format(ex))
                        raise CommandError(ex)
                logger.info("SeenRegistration Delete {} {} Time: {}\n".format(
                            y, q, timer.get_elapsed()))

    def link_visited(self):
        # clean up after one year
        timer = Timer()
        cut_off_dt = self.get_cut_off_date()
        entries_to_delete = VisitedLinkNew.objects.filter(
            visit_date__lt=cut_off_dt)
        while entries_to_delete.exists():
            try:
                batch = entries_to_delete[:batch_size]
                batch.delete()
                time.sleep(1)
                entries_to_delete = entries_to_delete[batch_size:]
            except Exception as ex:
                logger.error("VisitedLinkNew delelte {}\n".format(ex))
                raise CommandError(ex)
        logger.info(
            "VisitedLinkNew Delete viewed before {} Time: {}\n".format(
                cut_off_dt, timer.get_elapsed()))
