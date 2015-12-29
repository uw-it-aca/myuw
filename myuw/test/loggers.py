from django.test import TestCase
from myuw.logger.session_log import log_session
from django.test.client import RequestFactory


class TestSessionLog(TestCase):
    def test_mywm_2436(self):
        log_session('', None, RequestFactory().get("/"))
