from django.test import TestCase
from django.conf import settings
from myuw.views.page import _is_mobile
from django.test.client import RequestFactory


class TestPageMethods(TestCase):
    def test_mobile_check(self):
        request = RequestFactory().get("/",
                                       HTTP_USER_AGENT='Fake iPhone Agent')
        self.assertTrue(_is_mobile(request))

        request = RequestFactory().get("/",
                                       HTTP_USER_AGENT='Fake Android Mobile')
        self.assertTrue(_is_mobile(request))

        request = RequestFactory().get("/",
                                       HTTP_USER_AGENT='Fake Android Agent')
        self.assertFalse(_is_mobile(request))

        request = RequestFactory().get("/", HTTP_USER_AGENT=None)
        self.assertFalse(_is_mobile(request))
