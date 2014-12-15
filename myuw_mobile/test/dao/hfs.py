from django.test import TestCase

from myuw_mobile.dao.hfs import get_account_balances_by_uwnetid


class TestHFS(TestCase):

    def test_get_account_balance(self):
        self.assertEquals(get_account_balances_by_uwnetid(None), None)
        accounts = get_account_balances_by_uwnetid('javerage')
        self.assertEquals(accounts.student_husky_card.balance, 1.23)
        #Missing account
        self.assertEquals(get_account_balances_by_uwnetid("123notanetid"), None)