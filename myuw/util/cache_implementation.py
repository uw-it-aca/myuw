from django.conf import settings
import re
from rc_django.cache_implementation import TimedCache
from rc_django.cache_implementation.memcache import MemcachedCache
import memcache
import threading

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
        return ONE_HOUR

    if "uwnetid" == service:
        return FOUR_HOURS

    return FOUR_HOURS


class MyUWMemcachedCache(MemcachedCache):

    def get_cache_expiration_time(self, service, url):
        return get_cache_time(service, url)


class PythonMemcachedCache(MyUWMemcachedCache):
    def _set_client(self):
        thread_id = threading.current_thread().ident
        if not hasattr(PythonMemcachedCache, "_memcached_cache"):
            PythonMemcachedCache._memcached_cache = {}

        if thread_id in PythonMemcachedCache._memcached_cache:
            self.client = PythonMemcachedCache._memcached_cache[thread_id]
            return

        servers = settings.RESTCLIENTS_MEMCACHED_SERVERS

        self.client = memcache.Client(servers)
        PythonMemcachedCache._memcached_cache[thread_id] = self.client


class MyUWCache(TimedCache):

    def getCache(self, service, url, headers):
        return self._response_from_cache(
            service, url, headers, get_cache_time(service, url))

    def processResponse(self, service, url, response):
        return self._process_response(service, url, response)
