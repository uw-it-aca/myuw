from django.test import TransactionTestCase
from myuw.models import User
from myuw.dao.user import get_user_model
from myuw.test import fdao_pws_override, get_request_with_user


@fdao_pws_override
class TestUserDao(TransactionTestCase):

    def test_get_user_model(self):
        req = get_request_with_user("javerage")
        with self.assertRaises(AttributeError):
            a = req.get("myuw_user_model")

        user = get_user_model(req)
        self.assertIsNotNone(req.myuw_user_model)
        self.assertEqual(user.uwnetid, "javerage")
        last_visit = user.last_visit
        self.assertIsNotNone(str(user))

        # second time use the myuw_user_model in req
        user = get_user_model(req)
        self.assertEqual(last_visit, user.last_visit)

        # netid change
        user.update_user('javg001')
        self.assertEqual(user.uwnetid, "javg001")

        user = User.get_user("javerage", ['javg001'])
        self.assertEqual(user.uwnetid, "javerage")
