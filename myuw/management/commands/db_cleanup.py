# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Clean up the entries no longer useful
"""

import logging
from datetime import timedelta
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
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
log_format = "Deleted {} entries, Time={} seconds"
duration = 52 * 7   # days
quarters = ["winter", "spring", "summer", "autumn"]
batch_size = 1000


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('name', choices=[
            'course', 'notice', 'registration', 'link_visited'],
            help="The table to check ")

    def handle(self, *args, **options):
        self.errors = []
        name = options['name']

        if self.action == 'course':
            self.course_display()
        if self.action == 'notice':
            self.notice_read()
        if self.action == 'registration':
            self.registration_seen()
        if self.action == 'link_visited':
            self.link_visited()

        if len(self.errors):
            send_mail("Clear Expired Django Session Weekly Cron",
                      "\n".join(self.errors),
                      "{}@uw.edu".format(get_cronjob_sender()),
                      ["{}@uw.edu".format(get_cronjob_recipient())])

    def ex_delete(self, batch, msg_format):
        timer = Timer()
        batch.delete()
        self.count += 1
        # time.sleep(1)
        logger.info(msg_format, self.count, timer.get_elapsed())

    def course_display(self):
        for y in range(2000, 2022):
            for q in quarters:
                for c in range(1, 9):
                    entries_to_delete = UserCourseDisplay.objects.filter(
                        year__lt=y, quarter=q, color_id=c)
                    self.count = 0
                    while entries_to_delete.exists():
                        try:
                            batch = entries_to_delete[:batch_size]
                            self.ex_delete(
                                batch,
                                "UserCourseDisplay Delete Batch {} {}\n")
                            entries_to_delete = entries_to_delete[batch_size:]
                        except Exception as ex:
                            msg = "{} Delete Batch {} - {}\n".format(
                                "UserCourseDisplay", self.count, ex)
                            logger.error(msg)
                            self.errors.append(msg)

    def notice_read(self):
        now = sws_now()
        cut_off_dt = now - timedelta(days=180)
        entries_to_delete = UserNotices.objects.filter(
            first_viewed__lt=cut_off_dt)
        self.count = 0
        while entries_to_delete.exists():
            try:
                batch = entries_to_delete[:batch_size]
                self.ex_delete(batch, "UserNotices Delete Batch {} {}\n")
                entries_to_delete = entries_to_delete[batch_size:]
            except Exception as ex:
                msg = "UserNotices Delete Batch {} - {}\n".format(
                    self.count, ex)
                logger.error(msg)
                self.errors.append(msg)

    def registration_seen(self):
        entries_to_delete = SeenRegistration.objects.all()
        self.count = 0
        while entries_to_delete.exists():
            try:
                batch = entries_to_delete[:batch_size]
                self.ex_delete(
                    batch, "SeenRegistration Delete Batch {} {}\n")
                entries_to_delete = entries_to_delete[batch_size:]
            except Exception as ex:
                msg = "SeenRegistration Delete Batch {} - {}\n".format(
                    self.count, ex)
                logger.error(msg)
                self.errors.append(msg)

    def link_visited(self):
        now = sws_now()
        cut_off_dt = now - timedelta(days=duration)
        entries_to_delete = VisitedLinkNew.objects.filter(
            visit_date__lt=cut_off_dt)
        self.count = 0
        while entries_to_delete.exists():
            try:
                batch = entries_to_delete[:batch_size]
                self.ex_delete(batch, "VisitedLinkNew Delete Batch {} {}\n")
                entries_to_delete = entries_to_delete[batch_size:]
            except Exception as ex:
                msg = "VisitedLinkNew Delete Batch {} - {}\n".format(
                    self.count, ex)
                logger.error(msg)
                self.errors.append(msg)
