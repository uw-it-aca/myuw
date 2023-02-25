# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from myuw.dao.pds import load_cache


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_cache()
