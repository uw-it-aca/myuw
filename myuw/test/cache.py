from datetime import timedelta
from unittest2 import skipIf
from django.test import TestCase
from django.conf import settings
from restclients.mock_http import MockHTTP
from restclients.models import CacheEntryTimed
from restclients.exceptions import DataFailureException
from restclients.dao import SWS_DAO
from myuw.util.cache_implementation import MyUWCache, get_cache_time,\
    MyUWMemcachedCache


SWS = 'restclients.dao_implementation.sws.File'
CACHE = 'myuw.util.cache_implementation.MyUWCache'
MEMCACHE = 'myuw.util.cache_implementation.MyUWMemcachedCache'
FIVE_SECONDS = 5
FIFTEEN_MINS = 60 * 15
ONE_HOUR = 60 * 60
FOUR_HOURS = 60 * 60 * 4
ONE_DAY = 60 * 60 * 24
ONE_WEEK = 60 * 60 * 24 * 7


class TestCustomCachePolicy(TestCase):

    def test_get_cache_time(self):
        self.assertEquals(get_cache_time(
                "sws", "/student/myuwcachetest1"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
                "sws", "/student/v5/term/2013,spring.json"), ONE_WEEK)
        self.assertEquals(get_cache_time(
                "sws", "/student/v5/term/current.json"), ONE_DAY)
        self.assertEquals(get_cache_time(
                "sws", "/student/v5/course"), ONE_HOUR)
        self.assertEquals(get_cache_time(
                "sws", "/student/v5/enrollment"), ONE_HOUR)
        self.assertEquals(get_cache_time(
                "sws", "/student/v5/notice"), ONE_HOUR)
        self.assertEquals(get_cache_time(
                "sws", "/student/v5/registration"), FIFTEEN_MINS)
        self.assertEquals(get_cache_time(
                "myplan", "/api/plan/"), FIVE_SECONDS)
        self.assertEquals(get_cache_time(
                "grad", "/services/students"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
                "iasystem", "/uw/api/v1/evaluation"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
                "iasystem", "/uwb/api/v1/evaluation"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
                "iasystem", "/uwt/api/v1/evaluation"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
                "digitlib", "/php/currics/service.php"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
                "uwnetid", "/nws/v1/uwnetid"), FOUR_HOURS)
        self.assertEquals(get_cache_time(
                "gws", "group_sws/v2/group"), FOUR_HOURS)

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
            # Cached response is returned after 3 hours and 58 minutes
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=(60 * 4)-2))
            cache_entry.save()

            response = cache.getCache('sws', '/student/myuwcachetest1', {})
            self.assertNotEquals(response, None)

            # Cached response is not returned after 4 hours and 1 minute
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=(60 * 4)+1))
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
                minutes=(60*24*7-1))
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
            cache_entry.time_saved = orig_time_saved - timedelta(days=1)
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
                                      timedelta(seconds=5))
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
                                      timedelta(minutes=15))
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
                                      timedelta(minutes=60))
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
                                      timedelta(minutes=60))
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
                                      timedelta(minutes=60))
            cache_entry.save()
            response = cache.getCache('sws', '/student/v5/notice/xx', {})
            self.assertEquals(response, None)

    @skipIf(not getattr(settings, 'RESTCLIENTS_TEST_MEMCACHED', False),
            "Needs configuration to test memcached cache")
    def test_calling_myuw_get_cache_expiration_time(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=MEMCACHE,
                           RESTCLIENTS_SWS_DAO_CLASS=SWS):
            cache = MyUWMemcachedCache()
            c_entry = cache.getCache(
                'sws', '/student/v5/term/2013,summer.json', {})
            self.assertIsNone(c_entry)
            sws = SWS_DAO()
            response = None
            try:
                response = sws.getURL('/student/v5/term/2013,summer.json', {})
            except DataFailureException as ex:
                self.assertEquals(ex.msg, "MyUWMemcachedCache")
                self.assertIsNone(response)
