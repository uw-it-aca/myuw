# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management import call_command
from django.test import TestCase


class TestFlushMemcache(TestCase):

    def test_run(self):
        call_command('memcache', '-f')
        call_command('memcache', '--flush')
        call_command('memcache')
