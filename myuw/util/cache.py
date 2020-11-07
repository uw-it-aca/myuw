from datetime import date, datetime
import re
from uw_sws.term import get_term_by_date
from memcached_clients import RestclientPymemcacheClient

FIVE_SECONDS = 5
FIFTEEN_MINS = 60 * 15
HALF_HOUR = FIFTEEN_MINS * 2
ONE_HOUR = HALF_HOUR * 2
FOUR_HOURS = ONE_HOUR * 4
ONE_DAY = ONE_HOUR * 24


class MyUWMemcachedCache(RestclientPymemcacheClient):
    def get_cache_expiration_time(self, service, url, status=None):
        
        medium_expiration = (
            HALF_HOUR if during_peak_load(datetime.now())
                else FIFTEEN_MINS)

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
                return short_expiration

            return short_expiration

        if "kws" == service:
            if re.match(r'^/key/v1/encryption/', url):
                return ONE_DAY * 30
            return ONE_DAY * 7

        if "uwidp" == service:
            if re.match(r'^/idp/profile/oidc/keyset', url):
                return ONE_DAY

        if "gws" == service:
            return short_expiration

        if "pws" == service:
            return ONE_HOUR

        if "uwnetid" == service:
            return FOUR_HOURS

        return FOUR_HOURS


def during_peak_load(now):
    today = now.date()
    term = get_term_by_date(today)
    if (today >= term.registration_period1_start and
            today <= term.registration_period1_end):
        peak_start_time = datetime(now.year, now.month, now.day, 5, 30, 0)
        peak_end_time = datetime(now.year, now.month, now.day, 6, 30, 0)
        if (now >= peak_start_time and now <= peak_end_time):
            return True
    else:
        if (today == term.first_day_quarter)
            return True
    return False
