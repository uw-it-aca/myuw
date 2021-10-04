# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import timedelta
from unittest import skipIf
from django.test import TestCase
from django.conf import settings
from restclients_core.models import MockHTTP
from restclients_core.exceptions import DataFailureException
from uw_sws.dao import SWS_DAO
from uw_sws.util import fdao_sws_override
from myuw.util.cache import MyUWMemcachedCache


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
        self.assertEquals(cache.get_cache_expiration_time(
            "uwidp", "/idp/profile/oidc/keyset"), ONE_DAY)

        self.assertEquals(cache.get_cache_expiration_time(
            "myplan", "/api/plan/"), FIVE_SECONDS)

        self.assertEquals(cache.get_cache_expiration_time(
            "sws", "/student/v5/term/2013,spring.json"), ONE_DAY)
        self.assertEquals(cache.get_cache_expiration_time(
            "sws", "/student/v5/term/current.json"), ONE_DAY)
        self.assertEquals(cache.get_cache_expiration_time(
            "sws", "/student/v5/course/.../status.json"), FOUR_HOURS)
        self.assertEquals(cache.get_cache_expiration_time(
            "sws", "/student/v5/course/"), FIFTEEN_MINS)
        self.assertEquals(cache.get_cache_expiration_time(
            "sws", "/student/v5/person/"), ONE_HOUR)
        self.assertEquals(cache.get_cache_expiration_time(
            "sws", "/student/v5/enrollment"), FIFTEEN_MINS)
        self.assertEquals(cache.get_cache_expiration_time(
            "sws", "/student/v5/notice"), FIFTEEN_MINS)
        self.assertEquals(cache.get_cache_expiration_time(
            "sws", "/student/v5/registration"), FIFTEEN_MINS)
        self.assertEquals(cache.get_cache_expiration_time(
            "sws", "/student/v5/section"), FIFTEEN_MINS)

        self.assertEquals(cache.get_cache_expiration_time(
            "gws", "/group_sws/v3"), HALF_HOUR)

        self.assertEquals(cache.get_cache_expiration_time(
            "pws", "/nws/v1/uwnetid"), ONE_HOUR)
        self.assertEquals(cache.get_cache_expiration_time(
            "pws", "/nws/v1/uwnetid", status=404), 60 * 5)
        self.assertEquals(cache.get_cache_expiration_time(
            "uwnetid", "/nws/v1/uwnetid"), FOUR_HOURS)

        self.assertEquals(cache.get_cache_expiration_time(
            "grad", "/services/students"), FOUR_HOURS)
        self.assertEquals(cache.get_cache_expiration_time(
            "iasystem_uw", "/uw/api/v1/evaluation"), FOUR_HOURS)
        self.assertEquals(cache.get_cache_expiration_time(
            "iasystem_uwb", "/uwb/api/v1/evaluation"), FOUR_HOURS)
        self.assertEquals(cache.get_cache_expiration_time(
            "iasystem_uwt", "/uwt/api/v1/evaluation"), FOUR_HOURS)
        self.assertEquals(cache.get_cache_expiration_time(
            "digitlib", "/php/currics/service.php"), FOUR_HOURS)
        self.assertEquals(cache.get_cache_expiration_time(
            "kws", "/key/v1/encryption/"), ONE_DAY * 30)
        self.assertEquals(cache.get_cache_expiration_time(
            "kws", "/key/v1/type/"), ONE_DAY * 7)
