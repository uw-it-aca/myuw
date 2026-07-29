# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
import time
from unittest import skipIf, skipUnless

from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse

from myuw.test.api import missing_url
from myuw.util.cache import MyUWMemcachedCache


@override_settings(
    RESTCLIENTS_USE_THREADING=True,
    MYUW_PREFETCH_THREADING=True,
    RESTCLIENTS_DAO_CACHE_CLASS='myuw.util.cache.MyUWMemcachedCache',
    MEMCACHED_SERVERS=['memcached:11211'],
)
@skipIf(missing_url("myuw_home"), "myuw urls not configured")
@skipUnless(os.getenv("MEMCACHED_SERVER_COUNT"), "memcached not running")
class TestPageSpeeds(TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        MyUWMemcachedCache().flush_all()

    def test_index(self):
        url = reverse('myuw_home')
        t0 = time.time()
        resp = self.client.get(url, follow=True)
        t1 = time.time()

        delta = t1 - t0
        # With uncached resources
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(0.1 <= delta <= 0.3, f'Uncached time: {delta}')

        # With cached resources
        t2 = time.time()
        resp = self.client.get(url, follow=True)
        t3 = time.time()

        delta = t3 - t2
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(0.1 <= delta <= 0.2, f'Cached time: {delta}')
