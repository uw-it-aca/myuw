# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import skipIf
import time
from django.urls import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from myuw.test.api import missing_url, get_user, get_user_pass


class TestingMemoryCache(object):
    cache = {}

    def getCache(self, service, url, headers):
        key = self._get_key(service, url)
        if key in TestingMemoryCache.cache:
            return {"response": TestingMemoryCache.cache[key]}
        return None

    def processResponse(self, service, url, response):
        key = self._get_key(service, url)
        TestingMemoryCache.cache[key] = response

    def _get_key(self, service, url):
        return "%s__%s" % (service, url)

    @classmethod
    def clear_cache(cls):
        TestingMemoryCache.cache = {}


CACHE_DAO = 'myuw.test.speed.TestingMemoryCache'
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
        # Adding a little more - travis-ci is right on the line at 2.0
        # Adding a little more - travis with mysql just over 2.5, sqlite good
        self.assertLess(delta, 5)
