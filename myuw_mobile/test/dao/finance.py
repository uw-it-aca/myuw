from django.test import TestCase
from myuw_mobile.dao.finance import _get_account_balances_by_regid


class TestFinance(TestCase):

    def test_get_by_regid(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        finance = _get_account_balances_by_regid(regid)
        self.assertEquals(finance.tuition_accbalance, '12345.00')

        self.assertEquals(_get_account_balances_by_regid(None), None)

        self.assertEquals(_get_account_balances_by_regid("123"), None)
