# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django.core.management.base import BaseCommand
from myuw.dao.pds import (
    PDS_TYPE_STUD, PDS_TYPE_QUAR, get_cache_key, get_cached_data)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'systemkey', nargs='+', type=str, help="param1: systemkey")
        parser.add_argument(
            'scope', type=str, help="all|credits|quarters")

    def handle(self, *args, **options):
        system_key = options["systemkey"]
        scope = options["scope"]

        if scope == "credits" or scope == "all":
            data = get_cached_data(get_cache_key(PDS_TYPE_STUD, system_key))
            logger.info("{}: {}".format(PDS_TYPE_STUD, data))
        if scope == "quarters" or scope == "all":
            data = get_cached_data(get_cache_key(PDS_TYPE_QUAR, system_key))
            logger.info("{}: {}".format(PDS_TYPE_QUAR, data))
