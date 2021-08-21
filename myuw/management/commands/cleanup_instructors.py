# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from datetime import date
from django.core.management.base import BaseCommand
from myuw.models import Instructor

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    # clean up the instructor records no longer needed

    def handle(self, *args, **options):
        year = date.today().year - 6  # keep those within 6 years
        deleted = 0
        records = Instructor.objects.all()
        logger.info("Total records in Instructor table: {}".format(len(records)))
        for rec in records:
            if rec.year < year:
                Instructor.delete_seen_instructor(
                    rec.user, rec.year, rec.quarter)
                deleted += 1
        logger.info("Deleted {} records prior of {}".format(deleted, year))
