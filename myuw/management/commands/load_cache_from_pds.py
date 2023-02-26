# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django.core.management.base import BaseCommand, CommandError
from myuw.dao.pds import PdsClient

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        pds_client = PdsClient()
        pds_client.load_cache()
