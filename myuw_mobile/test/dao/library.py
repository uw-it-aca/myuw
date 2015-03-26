from django.test import TestCase
import datetime
from myuw_mobile.dao.library import _get_account_by_uwnetid


class TestLibrary(TestCase):

    def test_get_account_balance(self):
        self.assertEquals(_get_account_by_uwnetid(None), None)

        javerage_acct = _get_account_by_uwnetid('javerage')
        self.assertEquals(javerage_acct.next_due, datetime.date(2014, 5, 27))

        self.assertEquals(_get_account_by_uwnetid("123notarealuser"), None)
