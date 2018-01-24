from django.test import TestCase
from django.test.utils import override_settings
from myuw.logger.session_log import log_session
from myuw.test import get_request_with_user


UserService = 'userservice.user.UserServiceMiddleware'


@override_settings(MIDDLEWARE_CLASSES=(UserService))
class TestSessionLog(TestCase):
    def test_mywm_2436(self):
        netid = 'javerage'
        req = get_request_with_user(netid)
        log_session(netid, None, None, req)
