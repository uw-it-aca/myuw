# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django.core.management.base import BaseCommand
from myuw.dao.pds import get_cached_data

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'student_number', type=str, help="student_number")

    def handle(self, *args, **options):
        student_number = options["student_number"]

        data = get_cached_data(student_number)
        logger.info(data)
