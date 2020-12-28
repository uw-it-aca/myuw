from memcached_clients import RestclientPymemcacheClient
import re

FIVE_SECONDS = 5
FIFTEEN_MINS = 60 * 15
HALF_HOUR = 60 * 30
ONE_HOUR = 60 * 60
FOUR_HOURS = ONE_HOUR * 4
ONE_DAY = ONE_HOUR * 24


class MyUWMemcachedCache(RestclientPymemcacheClient):
    def get_cache_expiration_time(self, service, url, status=None):
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
            return HALF_HOUR

        if "pws" == service:
            return ONE_HOUR

        if "uwnetid" == service:
            return FOUR_HOURS

        return FOUR_HOURS
