# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from decimal import *
from restclients_core.exceptions import DataFailureException
from myuw.dao.hfs import get_account_balances_by_uwnetid
from myuw.test import fdao_hfs_override


@fdao_hfs_override
class TestHFS(TestCase):

    def test_get_account_balance(self):
        self.assertEqual(get_account_balances_by_uwnetid(None), None)

        accounts = get_account_balances_by_uwnetid('javerage')
        self.assertEqual(accounts.student_husky_card.balance, 1.23)
        self.assertEqual(
            accounts.student_husky_card.add_funds_url,
            "https://hfs.uw.edu/olco")
        # Testing case where json.loads poorly handles floats
        self.assertEqual(accounts.resident_dining.balance, 5.1)
        self.assertEqual(
            accounts.employee_husky_card.add_funds_url,
            "https://hfs.uw.edu/olco")

        # Missing account
        self.assertRaises(DataFailureException,
                          get_account_balances_by_uwnetid,
                          "123notanetid")

        self.assertRaises(DataFailureException,
                          get_account_balances_by_uwnetid,
                          "none")

        self.assertRaises(DataFailureException,
                          get_account_balances_by_uwnetid,
                          "jerror")
