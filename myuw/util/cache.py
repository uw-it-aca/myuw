# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from memcached_clients import RestclientPymemcacheClient
import re

FIVE_SECONDS = 5
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
            return FIVE_SECONDS

        if "sws" == service:
            if status and status != 200:
                if status >= 500:
                    return FIFTEEN_MINS
                return SEVEN_MINS

            if re.match(r'^/student/v5/term/', url):
                return ONE_DAY

            if re.match(r'^/student/v5/person/', url):
                return ONE_HOUR

            if re.match(r'^/student/v5/course/', url):
                if re.match(r'^/student/v5/course/.*/status.json$', url):
                    return FOUR_HOURS

            return FIFTEEN_MINS

        if "kws" == service:
            if re.match(r'^/key/v1/encryption/', url):
                return ONE_DAY * 30
            return ONE_DAY * 7

        if "uwidp" == service:
            if re.match(r'^/idp/profile/oidc/keyset', url):
                return ONE_DAY

        if "gws" == service:
            if status and status != 200:
                if status >= 500:
                    return FIFTEEN_MINS
                return SEVEN_MINS
            return HALF_HOUR

        if "pws" == service:
            if status and status != 200:
                if status >= 500:
                    return FIFTEEN_MINS
                return SEVEN_MINS
            return ONE_HOUR

        if "uwnetid" == service:
            if status and status != 200:
                if status >= 500:
                    return FIFTEEN_MINS
                return SEVEN_MINS
            return FOUR_HOURS

        return FOUR_HOURS
