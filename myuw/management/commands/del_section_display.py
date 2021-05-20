# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django.core.management.base import BaseCommand, CommandError
from myuw.models import User, UserCourseDisplay

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('netid', type=str,
                            help="param1: uwnetid")
        parser.add_argument('year', type=int,
                            help="param2: year")
        parser.add_argument('quarter', type=str,
                            help="param3: quarter")

    def handle(self, *args, **options):
        netid = options['netid']
        user = User.objects.get(uwnetid=netid)
        year = options['year']
        quarter = options['quarter']
        if user:
            objs = UserCourseDisplay.objects.filter(
                user=user, year=year, quarter=quarter).delete()

            for record in objs:
                logger.info("Deleted UserCourseDisplay {}" % record)
