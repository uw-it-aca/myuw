# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.finance import _get_account_balances_by_regid


class TestFinance(TestCase):

    def test_get_by_regid(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        finance = _get_account_balances_by_regid(regid)
        self.assertEqual(finance.tuition_accbalance, '12345.00')

        self.assertRaises(DataFailureException,
                          _get_account_balances_by_regid,
                          "none")

        self.assertRaises(DataFailureException,
                          _get_account_balances_by_regid,
                          "123")
