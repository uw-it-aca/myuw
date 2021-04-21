# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.core.management import call_command


class TestFlushMemcache(TestCase):

    def test_run(self):
        call_command('memcache', '-f')
        call_command('memcache', '--flush')
        call_command('memcache')
