# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from myuw.util.cache import MyUWMemcachedCache

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-f", "--flush",
                            action="store_true", default=False,
                            help="Flush the cache")

    def handle(self, *args, **options):
        flush = options["flush"]
        client = MyUWMemcachedCache()
        if flush:
            try:
                result = client.flush_all()
                logger.info(f"Flushed: {result}")
            except Exception as ex:
                logger.error(f"Memcached: {ex}, Servers: {settings.MEMCACHED_SERVERS}")
