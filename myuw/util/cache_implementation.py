from django.conf import settings
from django.utils import timezone
from restclients_core.models import MockHTTP
from rc_django.cache_implementation import TimedCache
from pymemcache.client.hash import HashClient
from pymemcache import serde
import threading
import json
import re

FIVE_SECONDS = 5
FIFTEEN_MINS = 60 * 15
ONE_HOUR = 60 * 60
FOUR_HOURS = ONE_HOUR * 4
ONE_DAY = ONE_HOUR * 24


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
                return FOUR_HOURS
            return FIFTEEN_MINS

        return FIFTEEN_MINS

    if "kws" == service:
        if re.match(r'^/key/v1/encryption/', url):
            return ONE_DAY * 30
        return ONE_DAY * 7

    if "uwidp" == service:
        if re.match(r'^/idp/profile/oidc/keyset', url):
            return ONE_DAY

    if "gws" == service:
        return FIFTEEN_MINS

    if "pws" == service:
        if re.match(r'^/idcard/v1/photo', url):
            return
        return ONE_HOUR

    if "uwnetid" == service:
        return FOUR_HOURS

    return FOUR_HOURS


class MyUWMemcachedCache(object):
    def __init__(self):
        self._set_client()

    def deleteCache(self, service, url):
        key = self._get_key(service, url)
        return self.client.delete(key)

    def getCache(self, service, url, headers):
        expire_seconds = self.get_cache_expiration_time(service, url)
        if expire_seconds is None:
            return

        key = self._get_key(service, url)
        data = self.client.get(key)

        if data:
            response = MockHTTP()
            response.headers = data.get("headers")
            response.status = data.get("status")
            response.data = data.get("data")
            return {"response": response}

    def processResponse(self, service, url, response):
        expire_seconds = self.get_cache_expiration_time(service, url)
        if expire_seconds is None:
            return

        header_data = {}
        for header in response.headers:
            header_data[header] = response.getheader(header)

        key = self._get_key(service, url)
        data = self._make_cache_data(
            response.data, header_data, response.status, timezone.now())
        self.client.set(key, data, expire=expire_seconds)

    def updateCache(self, service, url, new_data, new_data_dt):
        expire_seconds = self.get_cache_expiration_time(service, url)
        if expire_seconds is None:
            return

        key = self._get_key(service, url)
        data = self._make_cache_data(new_data, {}, 200, new_data_dt)
        self.client.replace(key, data, expire=expire_seconds)

    def get_cache_expiration_time(self, service, url):
        return get_cache_time(service, url)

    def _get_key(self, service, url):
        return "{}-{}".format(service, url)

    def _make_cache_data(self, data, headers, status, timestamp):
        return {
            "status": status,
            "headers": headers,
            "data": data,
            "time_stamp": timestamp.isoformat(),
        }

    def _set_client(self):
        thread_id = threading.current_thread().ident
        if not hasattr(MyUWMemcachedCache, "_memcached_cache"):
            MyUWMemcachedCache._memcached_cache = {}

        if thread_id in MyUWMemcachedCache._memcached_cache:
            self.client = MyUWMemcachedCache._memcached_cache[thread_id]
            return

        self.client = HashClient(
            settings.RESTCLIENTS_MEMCACHED_SERVERS,
            use_pooling=True,
            max_pool_size=settings.MEMCACHED_MAX_POOL_SIZE,
            connect_timeout=settings.MEMCACHED_CONNECT_TIMEOUT,
            timeout=settings.MEMCACHED_TIMEOUT,
            serde=serde.pickle_serde)
        MyUWMemcachedCache._memcached_cache[thread_id] = self.client


class MyUWCache(TimedCache):

    def getCache(self, service, url, headers):
        return self._response_from_cache(
            service, url, headers, get_cache_time(service, url))

    def processResponse(self, service, url, response):
        return self._process_response(service, url, response)
