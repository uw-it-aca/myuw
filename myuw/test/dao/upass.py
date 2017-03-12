from django.test import TestCase
from myuw.dao.upass import get_upass_by_netid
from myuw.test import fdao_upass_override, get_request_with_user


@fdao_upass_override
class TestUPassDao(TestCase):

    def test_get_by_netid(self):
        get_request_with_user("jnew")
        status = get_upass_by_netid("jnew")
        self.assertFalse(status.is_current)
        self.assertFalse(status.is_employee)
        self.assertTrue(status.is_student)

        get_request_with_user("botgrad")
        status = get_upass_by_netid("botgrad")
        self.assertTrue(status.is_current)
        self.assertFalse(status.is_employee)
        self.assertTrue(status.is_student)

        get_request_with_user("staff")
        status = get_upass_by_netid("staff")
        self.assertFalse(status.is_current)
        self.assertTrue(status.is_employee)
        self.assertFalse(status.is_student)
