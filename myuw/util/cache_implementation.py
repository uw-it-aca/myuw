import re
from django.conf import settings
from restclients.cache_implementation import MemcachedCache, TimedCache
from restclients.exceptions import DataFailureException


FIVE_SECONDS = 5
FIFTEEN_MINS = 60 * 15
ONE_HOUR = 60 * 60
FOUR_HOURS = 60 * 60 * 4
ONE_DAY = 60 * 60 * 24
ONE_WEEK = 60 * 60 * 24 * 7


def get_cache_time(service, url):
    if "myplan" == service:
        return FIVE_SECONDS

    if "sws" == service:
        if re.match('^/student/v5/term/current', url):
            return ONE_DAY

        if re.match('^/student/v5/term', url):
            return ONE_WEEK

        if re.match('^/student/v5/course', url) or\
                re.match('^/student/v5/enrollment', url) or\
                re.match('^/student/v5/notice', url):
            return ONE_HOUR

        if re.match('^/student/v5/registration', url):
            return FIFTEEN_MINS

    return FOUR_HOURS


class MyUWMemcachedCache(MemcachedCache):

    def get_cache_expiration_time(self, service, url):
        if getattr(settings, 'RESTCLIENTS_TEST_MEMCACHED', False):
            raise DataFailureException(url, 555, "MyUWMemcachedCache")
        return get_cache_time(service, url)


class MyUWCache(TimedCache):

    def getCache(self, service, url, headers):
        return self._response_from_cache(
            service, url, headers, get_cache_time(service, url))

    def processResponse(self, service, url, response):
        return self._process_response(service, url, response)


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
