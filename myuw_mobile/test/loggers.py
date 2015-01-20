from django.test import TestCase
from myuw_mobile.logger.session_log import log_session

class TestSessionLog(TestCase):
    def test_mywm_2436(self):
        log_session('', None, None)
