from django.test import TestCase
from myuw.logger.session_log import log_session
from django.test.client import RequestFactory
from django.test.utils import override_settings


UserService = 'userservice.user.UserServiceMiddleware'


@override_settings(MIDDLEWARE_CLASSES=(UserService))
class TestSessionLog(TestCase):
    def test_mywm_2436(self):
        log_session('', None, RequestFactory().get("/"))
