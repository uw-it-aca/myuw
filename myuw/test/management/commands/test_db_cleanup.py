# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch
from uw_sws.term import get_specific_term


class TestCheckResLinks(TestCase):

    @patch('myuw.dao.term.get_term_by_date', spec=True)
    def test_run(self, mock):
        mock.return_value = get_specific_term(2014, 'spring')
        call_command('db_cleanup', "course")
        call_command('db_cleanup', "seenreg")
        call_command('db_cleanup', "notice")
        call_command('db_cleanup', "linkvisit")
