# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from rc_django.cache_implementation import TimedCache
from myuw.util.cache import MyUWMemcachedCache


class MyUWCache(TimedCache):
    def getCache(self, service, url, headers):
        expires = MyUWMemcachedCache().get_cache_expiration_time(service, url)
        return self._response_from_cache(service, url, headers, expires)

    def processResponse(self, service, url, response):
        return self._process_response(service, url, response)
