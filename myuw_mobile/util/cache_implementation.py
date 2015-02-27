from restclients.cache_implementation import TimedCache
import re

FOUR_HOURS = 60 * 60 * 4
ONE_MONTH = 60 * 60 * 24 * 30

class MyUWCache(TimedCache):
    def getCache(self, service, url, headers):
        if "sws" == service:
            return self._getSWScache(url, headers)
        elif "myplan" == service:
            return self._getMyPlanCache(url, headers)

        return self._default(service, url, headers)

    def _getMyPlanCache(self, url, headers):
        return None

    def _getSWScache(self, url, headers):
        if re.match('^/student/v5/term', url):
            return self._response_from_cache('sws', url, headers, ONE_MONTH)
        return self._default('sws', url, headers)


    def _default(self, service, url, headers):
        return self._response_from_cache(service, url, headers, FOUR_HOURS)

    def processResponse(self, service, url, response):
        return self._process_response(service, url, response)
