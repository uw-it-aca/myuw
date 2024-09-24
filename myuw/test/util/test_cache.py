# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import timedelta
from unittest import skipIf
from django.test import TestCase
from django.conf import settings
from restclients_core.models import MockHTTP
from restclients_core.exceptions import DataFailureException
from uw_sws.dao import SWS_DAO
from uw_sws.util import fdao_sws_override
from myuw.util.cache import MyUWMemcachedCache, MyUWCache, IdPhotoToken


MEMCACHE = 'myuw.util.cache.MyUWMemcachedCache'
FIVE_SECONDS = 5
FIFTEEN_MINS = 60 * 15
HALF_HOUR = FIFTEEN_MINS * 2
ONE_HOUR = 60 * 60
FOUR_HOURS = ONE_HOUR * 4
ONE_DAY = ONE_HOUR * 24


@fdao_sws_override
class TestCustomCachePolicy(TestCase):

    def test_get_cache_time(self):
        cache = MyUWMemcachedCache()
        self.assertEqual(cache.get_cache_expiration_time(
            "uwidp", "/idp/profile/oidc/keyset"), ONE_DAY)

        self.assertEqual(cache.get_cache_expiration_time(
            "myplan", "/api/plan/"), FIVE_SECONDS)
        self.assertEqual(cache.get_cache_expiration_time(
            "myplan_auth", "/oauth2/token"), 60 * 45)
        self.assertEqual(cache.get_cache_expiration_time(
            "sws", "/student/v5/term/2013,spring.json"), ONE_DAY)
        self.assertEqual(cache.get_cache_expiration_time(
            "sws", "/student/v5/term/current.json"), ONE_DAY)
        self.assertEqual(cache.get_cache_expiration_time(
            "sws", "/student/v5/course/.../status.json"), FOUR_HOURS)
        self.assertEqual(cache.get_cache_expiration_time(
            "sws", "/student/v5/course/"), FIFTEEN_MINS)
        self.assertEqual(cache.get_cache_expiration_time(
            "sws", "/student/v5/person/"), ONE_HOUR)
        self.assertEqual(cache.get_cache_expiration_time(
            "sws", "/student/v5/enrollment"), FIFTEEN_MINS)
        self.assertEqual(cache.get_cache_expiration_time(
            "sws", "/student/v5/notice"), FIFTEEN_MINS)
        self.assertEqual(cache.get_cache_expiration_time(
            "sws", "/student/v5/registration"), FIFTEEN_MINS)
        self.assertEqual(cache.get_cache_expiration_time(
            "sws", "/student/v5/section"), FIFTEEN_MINS)
        self.assertEqual(cache.get_cache_expiration_time(
            "sws", "/student/v5/section", status=404), 60 * 7)
        self.assertEqual(cache.get_cache_expiration_time(
            "sws", "/student/v5/section", status=503), 60 * 15)

        self.assertEqual(cache.get_cache_expiration_time(
            "gws", "/group_sws/v3"), HALF_HOUR)
        self.assertEqual(cache.get_cache_expiration_time(
            "gws", "/group_sws/v3", status=404), 60 * 7)
        self.assertEqual(cache.get_cache_expiration_time(
            "gws", "/group_sws/v3", status=500), 60 * 15)

        self.assertEqual(cache.get_cache_expiration_time(
            "pws", "/identity/v2/person"), ONE_HOUR)
        self.assertEqual(cache.get_cache_expiration_time(
            "pws", "/identity/v2/person", status=404), 60 * 7)
        self.assertEqual(cache.get_cache_expiration_time(
            "pws", "/identity/v2/person", status=503), 60 * 15)

        self.assertEqual(cache.get_cache_expiration_time(
            "uwnetid", "/nws/v1/uwnetid"), FOUR_HOURS)
        self.assertEqual(cache.get_cache_expiration_time(
            "uwnetid", "/nws/v1/uwnetid", status=404), 60 * 7)
        self.assertEqual(cache.get_cache_expiration_time(
            "uwnetid", "/nws/v1/uwnetid", status=409), 60 * 7)
        self.assertEqual(cache.get_cache_expiration_time(
            "uwnetid", "/nws/v1/uwnetid", status=500), 60 * 15)

        self.assertEqual(cache.get_cache_expiration_time(
            "grad", "/services/students"), FOUR_HOURS)
        self.assertEqual(cache.get_cache_expiration_time(
            "iasystem_uw", "/uw/api/v1/evaluation"), FOUR_HOURS)
        self.assertEqual(cache.get_cache_expiration_time(
            "iasystem_uwb", "/uwb/api/v1/evaluation"), FOUR_HOURS)
        self.assertEqual(cache.get_cache_expiration_time(
            "iasystem_uwt", "/uwt/api/v1/evaluation"), FOUR_HOURS)
        self.assertEqual(cache.get_cache_expiration_time(
            "digitlib", "/php/currics/service.php"), FOUR_HOURS)
        self.assertEqual(cache.get_cache_expiration_time(
            "kws", "/key/v1/encryption/"), ONE_DAY * 30)
        self.assertEqual(cache.get_cache_expiration_time(
            "kws", "/key/v1/type/"), ONE_DAY * 7)

        self.assertEqual(cache.get_cache_expiration_time(
            "mailman", "/uw_list_manager/api/v1/list/"), ONE_DAY)
        self.assertEqual(cache.get_cache_expiration_time(
            "mailman", "/uw_list_manager/api/v1/list/", status=404), 60 * 7)
        self.assertEqual(cache.get_cache_expiration_time(
            "mailman", "/uw_list_manager/api/v1/list/", status=500), 60 * 15)

        self.assertEqual(cache.get_cache_expiration_time(
            "uwidp", "/idp/profile/oidc/keyset", status=404), 60 * 7)
        self.assertEqual(cache.get_cache_expiration_time(
            "uwidp", "/idp/profile/oidc/keyset", status=500), 60 * 15)


class TestMyUWCache(TestCase):

    def test_cache(self):
        cache = MyUWCache()
        self.assertEqual(
            cache.cache_key("test", "1"), "test-key-1")
        self.assertEqual(
            cache.get_cache_expiration(), 60 * 7)
        cache.cache_set("test-key-1", {"name": 1})
        self.assertEqual(
            cache.cache_get("test-key-1"), {"name": 1})


class test_IdPhotoToken(TestCase):
    def test_cache(self):
        ipt = IdPhotoToken()
        self.assertEqual(ipt.get_key("1"), "idphoto-key-1")
        token = ipt.get_token()
        self.assertTrue(ipt.valid_token(token))
