# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django.core.management.base import BaseCommand, CommandError
from myuw.dao.pds import (
    PDS_TYPE_STUD, PDS_TYPE_QUAR, PdsClient, get_cached_data)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'scope', type=str,
            help="{}|{}|all".format(PDS_TYPE_STUD, PDS_TYPE_QUAR))

    def handle(self, *args, **options):
        scope = options["scope"]
        pds_client = PdsClient()
        if scope == PDS_TYPE_STUD or scope == "all":
            pds_client.get_application_type_credits()
        if scope == PDS_TYPE_QUAR or scope == "all":
            pds_client.get_quarters_completed()
