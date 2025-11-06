# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import random
import string
from django.core.cache import cache
from memcached_clients import RestclientPymemcacheClient
import re

FEW_SECONDS = 10
SEVEN_MINS = 60 * 7
FIFTEEN_MINS = 60 * 15
HALF_HOUR = 60 * 30
ONE_HOUR = 60 * 60
FOUR_HOURS = ONE_HOUR * 4
ONE_DAY = ONE_HOUR * 24


class MyUWMemcachedCache(RestclientPymemcacheClient):
    def get_cache_expiration_time(self, service, url, status=None):
        if "myplan_auth" == service:
            return FIFTEEN_MINS * 3

        if "myplan" == service:
            return FEW_SECONDS

        if status and status != 200:
            return SEVEN_MINS

        if "sws" == service:
            if re.match(r'^/student/v5/term/', url):
                return ONE_DAY

            if re.match(r'^/student/v5/person/', url):
                return ONE_HOUR

            if re.match(r'^/student/v5/course/', url):
                return ONE_HOUR

            return FIFTEEN_MINS

        if "kws" == service:
            if re.match(r'^/key/v1/encryption/', url):
                return ONE_DAY * 30
            return ONE_DAY * 7

        if "uwidp" == service:
            if re.match(r'^/idp/profile/oidc/keyset', url):
                return ONE_DAY

        if "gws" == service:
            return HALF_HOUR

        if "pws" == service:
            return ONE_HOUR

        if "uwnetid" == service:
            return FOUR_HOURS

        if "mailman" == service:
            return ONE_DAY

        return FOUR_HOURS


class MyUWCache():
    def cache_key(self, service, token):
        return f"{service}-key-{token}"

    def get_cache_expiration(self):
        return SEVEN_MINS

    def cache_get(self, key):
        return cache.get(key)

    def cache_set(self, key, value):
        cache.set(key, value, timeout=self.get_cache_expiration())


class IdPhotoToken(MyUWCache):

    def get_key(self, token):
        return self.cache_key("idphoto", token)

    def get_token(self):
        data = {'token_size': 16}
        token = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(16))
        self.cache_set(self.get_key(token), data)
        return token

    def valid_token(self, token):
        return self.cache_get(self.get_key(token)) is not None
