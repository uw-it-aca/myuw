from django.test import TransactionTestCase
from myuw.models import User
from myuw.dao.user import get_user_model
from myuw.test import fdao_pws_override, get_request_with_user


@fdao_pws_override
class TestUserDao(TransactionTestCase):

    def test_get_user_model(self):
        req = get_request_with_user("javerage")
        # cached attribute doesn't exists
        with self.assertRaises(AttributeError):
            a = req.get("myuw_user_model")

        user = get_user_model(req)
        self.assertIsNotNone(req.myuw_user_model)
        self.assertEqual(user.uwnetid, "javerage")
        self.assertTrue(user.is_netid_changed("jav"))
        self.assertIsNotNone(str(user))
        last_visit = user.last_visit

        # second time use the myuw_user_model in req
        user = get_user_model(req)
        self.assertEqual(last_visit, user.last_visit)

        # doesn't change last_visit value
        self.assertTrue(User.exists("javerage"))
        user = User.get_user_by_netid("javerage")
        self.assertEqual(user.last_visit, last_visit)

        # netid change, update last_visit value
        user1 = User.update("javerage", "javg001")
        self.assertFalse(user1 == user)
        self.assertNotEqual(last_visit, user1.last_visit)
        last_visit = user.last_visit

        # get by current and prior netids (update last_visit value)
        user = User.get_user("javerage", ['javg001'])
        self.assertEqual(user.uwnetid, "javerage")
        self.assertNotEqual(last_visit, user.last_visit)
        last_visit = user.last_visit

        user = User.get_user("javerage")
        user.delete()
        user = User.get_user("javerage", ['javg001'])
        self.assertEqual(user.uwnetid, "javerage")
        self.assertNotEqual(last_visit, user.last_visit)
