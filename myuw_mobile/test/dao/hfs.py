from django.test import TestCase
from decimal import *
from myuw_mobile.dao.hfs import get_account_balances_by_uwnetid


class TestHFS(TestCase):

    def test_get_account_balance(self):
        self.assertEquals(get_account_balances_by_uwnetid(None), None)
        accounts = get_account_balances_by_uwnetid('javerage')
        self.assertEquals(accounts.student_husky_card.balance, Decimal('1.23'))
        # Testing case where json.loads poorly handles floats
        self.assertEquals(accounts.resident_dining.balance, Decimal('5.1'))

        #Missing account
        self.assertEquals(get_account_balances_by_uwnetid("123notanetid"), None)