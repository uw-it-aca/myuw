import re
from restclients.cache_implementation import MemcachedCache, TimedCache


FIVE_SECONDS = 5
FIFTEEN_MINS = 60 * 15
ONE_HOUR = 60 * 60
FOUR_HOURS = 60 * 60 * 4
ONE_DAY = 60 * 60 * 24
ONE_WEEK = 60 * 60 * 24 * 7


def get_myuw_sws_cache_time(url):
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

    # person, AccountBalance
    return FOUR_HOURS


class MyUWMemcachedCache(MemcachedCache):

    def _get_time(self, service, url):
        if "myplan" == service:
            return FIVE_SECONDS

        if "sws" == service:
            return get_myuw_sws_cache_time(url)

        return FOUR_HOURS


class MyUWCache(TimedCache):

    def getCache(self, service, url, headers):
        if "myplan" == service:
            return self._response_from_cache(
                service, url, headers, FIVE_SECONDS)

        if "sws" == service:
            return self._response_from_cache(
                service, url, headers, get_myuw_sws_cache_time(url))

        return self._response_from_cache(service, url, headers, FOUR_HOURS)

    def processResponse(self, service, url, response):
        return self._process_response(service, url, response)
