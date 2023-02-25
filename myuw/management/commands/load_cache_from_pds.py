# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django.core.management.base import BaseCommand, CommandError
from myuw.dao.pds import PdsClient

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'scope', type=str, help="all|credits|quarters")

    def handle(self, *args, **options):
        scope = options["scope"]
        pds_client = PdsClient()
        if scope == "credits" or scope == "all":
            pds_client.get_application_type_credits()
        if scope == "quarters" or scope == "all":
            pds_client.get_quarters_completed()
