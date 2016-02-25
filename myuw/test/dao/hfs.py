from django.test import TestCase
from decimal import *
from restclients.exceptions import DataFailureException
from myuw.dao.hfs import get_account_balances_by_uwnetid


class TestHFS(TestCase):

    def test_get_account_balance(self):
        self.assertEquals(get_account_balances_by_uwnetid(None), None)

        accounts = get_account_balances_by_uwnetid('javerage')
        self.assertEquals(accounts.student_husky_card.balance, Decimal('1.23'))
        self.assertEquals(
            accounts.student_husky_card.add_funds_url,
            "https://www.hfs.washington.edu/olco/Secure/AccountSummary.aspx")
        # Testing case where json.loads poorly handles floats
        self.assertEquals(accounts.resident_dining.balance, Decimal('5.1'))
        self.assertEquals(
            accounts.employee_husky_card.add_funds_url,
            "https://www.hfs.washington.edu/olco/Secure/AccountSummary.aspx")

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
