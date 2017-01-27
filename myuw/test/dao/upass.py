from django.test import TestCase
from myuw.dao.upass import get_upass_by_netid
from myuw.test import get_request


class TestUPassDao(TestCase):
    def setUp(self):
        get_request()

    def test_get_by_netid(self):
        status = get_upass_by_netid("javerage")

        self.assertFalse(status.is_staff)
        self.assertTrue(status.is_student)
        self.assertTrue(status.is_active)
