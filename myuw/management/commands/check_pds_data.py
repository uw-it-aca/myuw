# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import json
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
        j = json.loads(data)
        application_status_code = int(j["application_status_code"])
        logger.info("Transfer student: {}".format(
            application_status_code == 2 or application_status_code == 4
        ))
        total_deductible_credits = float(j["total_deductible_credits"])
        total_extension_credits = float(j["total_extension_credits"])
        total_grade_attempted = float(j["total_grade_attempted"])
        total_lower_div_transfer_credits = float(j["total_lower_div_transfer_credits"])
        total_upper_div_transfer_credits = float(j["total_upper_div_transfer_credits"])
        total_non_graded_credits = float(j["total_non_graded_credits"])
        total_credit = (
            total_grade_attempted +
            total_non_graded_credits +
            total_lower_div_transfer_credits +
            total_upper_div_transfer_credits +
            total_extension_credits) -
            total_deductible_credits
        logger.info("credits toward degree: {}".format(total_credit))
