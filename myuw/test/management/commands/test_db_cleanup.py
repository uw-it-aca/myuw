# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.core.management import call_command


class TestCheckResLinks(TestCase):

    def test_run(self):
        call_command('db_cleanup', "course")
        call_command('db_cleanup', "seenreg")
        call_command('db_cleanup', "notice")
        call_command('db_cleanup', "linkvisit")
