from django.test import TransactionTestCase
from myuw.dao import get_user_model
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestDaoInit(TransactionTestCase):

    def test_get_user_model(self):
        req = get_request_with_user("javerage")
        user = get_user_model(req)
        self.assertEqual(user.uwnetid, "javerage")
        self.assertIsNotNone(user.last_visit)
        self.assertIsNotNone(user.json_data())
        self.assertIsNotNone(user.__str__())
