import logging
import json
import re
from base64 import b64encode
from bmemcached.exceptions import MemcachedException
from django.conf import settings
from rc_django.cache_implementation import MemcachedCache, TimedCache
from restclients_core.exceptions import DataFailureException


FIVE_SECONDS = 5
FIFTEEN_MINS = 60 * 15
ONE_HOUR = 60 * 60
FOUR_HOURS = 60 * 60 * 4
ONE_DAY = 60 * 60 * 24
logger = logging.getLogger(__name__)


def get_cache_time(service, url):
    if "myplan" == service:
        return FIVE_SECONDS

    if "sws" == service:
        if re.match(r'^/student/v5/term/', url):
            return ONE_DAY

        if re.match(r'^/student/v5/person/', url):
            return ONE_HOUR

        if re.match(r'^/student/v5/course/', url):
            if re.match(r'^/student/v5/course/.*/status.json$', url):
                return ONE_HOUR
            return FIFTEEN_MINS * 2

        return FIFTEEN_MINS

    if "kws" == service:
        if re.match(r'^"/key/v1/encryption/', url):
            return ONE_DAY * 30
        return ONE_DAY * 7

    if "gws" == service:
        return FIFTEEN_MINS

    if "pws" == service:
        return ONE_HOUR

    if "uwnetid" == service:
        return ONE_HOUR

    return FOUR_HOURS


class MyUWMemcachedCache(MemcachedCache):

    def get_cache_expiration_time(self, service, url):
        if getattr(settings, 'RESTCLIENTS_TEST_MEMCACHED', False):
            raise DataFailureException(url, 555, "MyUWMemcachedCache")
        return get_cache_time(service, url)

    def update_cache(self, service, url, new_json_data):
        client = self._get_client()
        key = self._get_key(service, url)

        # clear existing data
        try:
            value = client.get(key)

            if value:
                client.delete(key)
                # may raise MemcachedException
                logger.info("IN cache (key: %s), DELETED", key)
            else:
                logger.info("NOT IN cache (key: %s)", key)

        except MemcachedException as ex:
            logger.info("Failed to clear existing data(key=%s) ==> %s",
                        key, ex)
            return

        # store new value in cache
        data = json.dumps({
            "status": 200,
            "b64_data": b64encode(json.dumps(new_json_data)),
            "headers": {}})

        time_to_store = self.get_cache_expiration_time(service, url)

        client.set(key, data, time=time_to_store)
        # may raise MemcachedException
        logger.info("MemCached SET with key %s for %d seconds",
                    key, time_to_store)


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

    @classmethod
    def clear_cache(cls):
        TestingMemoryCache.cache = {}
