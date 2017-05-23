from django.test import TestCase
from myuw.dao.uwnetid import is_clinician, is_faculty
from myuw.test import (fdao_uwnetid_override,
                       get_request, get_request_with_user)


@fdao_uwnetid_override
class TestUWNetid(TestCase):
    def setUp(self):
        get_request()

    def test_is_faculty(self):
        get_request_with_user('bill')
        self.assertTrue(is_faculty())

    def test_is_clinician(self):
        get_request_with_user('eight')
        self.assertTrue(is_clinician())
