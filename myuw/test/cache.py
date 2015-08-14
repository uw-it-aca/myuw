from django.test import TestCase
from restclients.mock_http import MockHTTP
from myuw.util.cache_implementation import MyUWCache
from restclients.models import CacheEntryTimed
from datetime import timedelta


CACHE = 'myuw.util.cache_implementation.MyUWCache'


class TestCustomCachePolicy(TestCase):
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
            # Cached response is returned after 29 days
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = orig_time_saved - timedelta(days=29)
            cache_entry.save()

            response = cache.getCache(
                'sws', '/student/v5/term/1014,summer.json', {})
            self.assertNotEquals(response, None)

            # Cached response is not returned after 31 days
            cache_entry.time_saved = orig_time_saved - timedelta(days=31)
            cache_entry.save()

            response = cache.getCache(
                'sws', '/student/v5/term/1014,summer.json', {})
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
            self.assertEquals(response, None)

    def test_default_policies(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('no_such', '/student/myuwcachetest1', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "no_such", "/student/myuwcachetest1", ok_response)
            response = cache.getCache('no_such', '/student/myuwcachetest1', {})
            self.assertEquals(response["response"].data, 'xx')

            cache_entry = CacheEntryTimed.objects.get(
                service="no_such", url="/student/myuwcachetest1")
            # Cached response is returned after 3 hours and 58 minutes
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=(60 * 4)-2))
            cache_entry.save()

            response = cache.getCache('no_such', '/student/myuwcachetest1', {})
            self.assertNotEquals(response, None)

            # Cached response is not returned after 4 hours and 1 minute
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=(60 * 4)+1))
            cache_entry.save()

            response = cache.getCache('no_such', '/student/myuwcachetest1', {})
            self.assertEquals(response, None)
