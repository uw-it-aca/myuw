from datetime import timedelta
from unittest import skipIf
from django.test import TestCase
from django.conf import settings
from restclients_core.models import MockHTTP
from rc_django.models import CacheEntryTimed
from restclients_core.exceptions import DataFailureException
from uw_sws.dao import SWS_DAO
from uw_sws.util import fdao_sws_override
from myuw.util.cache_implementation import MyUWCache, get_cache_time,\
    MyUWMemcachedCache


CACHE = 'myuw.util.cache_implementation.MyUWCache'
MEMCACHE = 'myuw.util.cache_implementation.MyUWMemcachedCache'
FIVE_SECONDS = 5
FIFTEEN_MINS = 60 * 15
ONE_HOUR = 60 * 60
FOUR_HOURS = ONE_HOUR * 4
ONE_DAY = ONE_HOUR * 24


@fdao_sws_override
class TestCustomCachePolicy(TestCase):

    def test_get_cache_time(self):
        self.assertEquals(get_cache_time(
            "uw_idp", "/idp/profile/oidc/"), FIVE_SECONDS)

        self.assertEquals(get_cache_time(
            "myplan", "/api/plan/"), FIVE_SECONDS)

        self.assertEquals(get_cache_time(
            "sws", "/student/v5/term/2013,spring.json"), ONE_DAY)
        self.assertEquals(get_cache_time(
            "sws", "/student/v5/term/current.json"), ONE_DAY)
        self.assertEquals(get_cache_time(
            "sws", "/student/v5/course/.../status.json"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
            "sws", "/student/v5/course/"), FIFTEEN_MINS)
        self.assertEquals(get_cache_time(
            "sws", "/student/v5/person/"), ONE_HOUR)
        self.assertEquals(get_cache_time(
            "sws", "/student/v5/enrollment"), FIFTEEN_MINS)
        self.assertEquals(get_cache_time(
            "sws", "/student/v5/notice"), FIFTEEN_MINS)
        self.assertEquals(get_cache_time(
            "sws", "/student/v5/registration"), FIFTEEN_MINS)
        self.assertEquals(get_cache_time(
            "sws", "/student/v5/section"), FIFTEEN_MINS)

        self.assertEquals(get_cache_time(
            "gws", "/group_sws/v3"), FIFTEEN_MINS)

        self.assertEquals(get_cache_time(
            "pws", "/nws/v1/uwnetid"), ONE_HOUR)
        self.assertEquals(get_cache_time(
            "uwnetid", "/nws/v1/uwnetid"), FOUR_HOURS)

        self.assertEquals(get_cache_time(
            "grad", "/services/students"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
            "iasystem_uw", "/uw/api/v1/evaluation"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
            "iasystem_uwb", "/uwb/api/v1/evaluation"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
            "iasystem_uwt", "/uwt/api/v1/evaluation"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
            "digitlib", "/php/currics/service.php"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
            "kws", "/key/v1/encryption/"), ONE_DAY * 30)
        self.assertEquals(get_cache_time(
            "kws", "/key/v1/type/"), ONE_DAY * 7)

    def test_sws_default_policies(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('sws', '/student/myuwcachetest1', {})
            self.assertEquals(response, None)
            cache.processResponse("sws",
                                  "/student/myuwcachetest1",
                                  ok_response)
            response = cache.getCache('sws', '/student/myuwcachetest1', {})
            self.assertEquals(response["response"].data, 'xx')

            cache_entry = CacheEntryTimed.objects.get(
                service="sws",
                url="/student/myuwcachetest1")
            # Cached response is returned before 15 minutes
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=14))
            cache_entry.save()

            response = cache.getCache('sws', '/student/myuwcachetest1', {})
            self.assertNotEquals(response, None)

            # Cached response is not returned after 15 minute
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=16))
            cache_entry.save()

            response = cache.getCache('sws', '/student/myuwcachetest1', {})
            self.assertEquals(response, None)

    def test_sws_term_policy(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache(
                'sws', '/student/v5/term/1014,summer.json', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/term/1014,summer.json", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/term/1014,summer.json', {})
            self.assertEquals(response["response"].data, 'xx')

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/term/1014,summer.json")
            # Cached response is returned after 6 days
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = orig_time_saved - timedelta(
                minutes=(60*24-1))
            cache_entry.save()

            response = cache.getCache(
                'sws', '/student/v5/term/1014,summer.json', {})
            self.assertNotEquals(response, None)

            # Cached response is not returned after 7 days
            cache_entry.time_saved = orig_time_saved - timedelta(days=7)
            cache_entry.save()

            response = cache.getCache(
                'sws', '/student/v5/term/current.json', {})
            self.assertEquals(response, None)

            response = cache.getCache(
                'sws', '/student/v5/term/current.json', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/term/current.json", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/term/current.json', {})
            self.assertEquals(response["response"].data, 'xx')

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/term/current.json")
            # Cached response is returned after 6 days
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = orig_time_saved - timedelta(
                minutes=(60*24-1))
            cache_entry.save()

            response = cache.getCache(
                'sws', '/student/v5/term/current.json', {})
            self.assertNotEquals(response, None)

            # Cached response is not returned after 7 days
            cache_entry.time_saved = orig_time_saved - timedelta(days=2)
            cache_entry.save()

            response = cache.getCache(
                'sws', '/student/v5/term/current.json', {})
            self.assertEquals(response, None)

    def test_myplan_default(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('myplan', '/api/plan/xx', {})
            self.assertEquals(response, None)
            cache.processResponse("myplan", "/api/plan/xx", ok_response)
            response = cache.getCache('myplan', '/api/plan/xx', {})

            cache_entry = CacheEntryTimed.objects.get(
                service="myplan", url="/api/plan/xx")
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(seconds=6))
            cache_entry.save()
            response = cache.getCache('myplan', '/api/plan/xx', {})
            self.assertEquals(response, None)

    def test_registration_default(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('sws', '/student/v5/registration/xx', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/registration/xx", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/registration/xx', {})

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/registration/xx")
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=16))
            cache_entry.save()
            response = cache.getCache('sws', '/student/v5/registration/xx', {})
            self.assertEquals(response, None)

    def test_course_default(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('sws', '/student/v5/course/xx', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/course/xx", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/course/xx', {})

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/course/xx")
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=16))
            cache_entry.save()
            response = cache.getCache('sws', '/student/v5/course/xx', {})
            self.assertEquals(response, None)

    def test_enrollment_default(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('sws', '/student/v5/enrollment/xx', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/enrollment/xx", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/enrollment/xx', {})

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/enrollment/xx")
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=16))
            cache_entry.save()
            response = cache.getCache('sws', '/student/v5/enrollment/xx', {})
            self.assertEquals(response, None)

    def test_notice_default(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('sws', '/student/v5/notice/xx', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/notice/xx", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/notice/xx', {})

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/notice/xx")
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=16))
            cache_entry.save()
            response = cache.getCache('sws', '/student/v5/notice/xx', {})
            self.assertEquals(response, None)

    def test_myuwmemcachedcache(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=MEMCACHE):
            cache = MyUWMemcachedCache()
            self.assertEquals(cache.get_cache_expiration_time(
                'sws', '/student/v5/term/2013,summer.json'), ONE_DAY)
