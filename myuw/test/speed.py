from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from myuw.test.api import missing_url, get_user, get_user_pass
from myuw.util.cache_implementation import TestingMemoryCache
from django.core.urlresolvers import reverse
from unittest2 import skipIf
import time


CACHE_DAO = 'myuw.util.cache_implementation.TestingMemoryCache'
FDAO_SWS = 'restclients.dao_implementation.sws.File'
Session = 'django.contrib.sessions.middleware.SessionMiddleware'
Common = 'django.middleware.common.CommonMiddleware'
CsrfView = 'django.middleware.csrf.CsrfViewMiddleware'
Auth = 'django.contrib.auth.middleware.AuthenticationMiddleware'
Message = 'django.contrib.messages.middleware.MessageMiddleware'
XFrame = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
UserService = 'userservice.user.UserServiceMiddleware'
AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'
DELAY = 0.5


@override_settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                   MIDDLEWARE_CLASSES=(Session,
                                       Common,
                                       CsrfView,
                                       Auth,
                                       Message,
                                       XFrame,
                                       UserService,
                                       ),
                   RESTCLIENTS_MOCKDATA_DELAY=DELAY,
                   RESTCLIENTS_USE_THREADING=True,
                   MYUW_PREFETCH_THREADING=True,
                   AUTHENTICATION_BACKENDS=(AUTH_BACKEND,),
                   RESTCLIENTS_DAO_CACHE_CLASS=CACHE_DAO,
                   )
class TestPageSpeeds(TestCase):
    @skipIf(missing_url("myuw_home"), "myuw urls not configured")
    def test_index(self):

        TestingMemoryCache.clear_cache()
        client = Client()
        get_user('javerage')
        client.login(username='javerage',
                     password=get_user_pass('javerage'))
        t0 = time.time()
        resp = client.get(reverse('myuw_home'))
        t1 = time.time()

        delta = t1-t0

        # Assert greater to make sure we're actually running the code.
        # There are 3 known rounds of requests made, which should take .5
        # seconds each
        self.assertGreater(delta, 1.5)
        # Make sure there aren't more requests made.  0.5 seconds should be
        # enough time to generate the view!
        self.assertLess(delta, 2.0)
