from myuw.util.cache import MyUWMemcachedCache
from memcached_clients.restclient import CachedHTTPResponse
from django.utils.timezone import localtime
from dateutil.parser import parse
import json


def update_sws_entry_in_cache(url, new_value, new_value_dt):
    """
    Updates a cached record, if the passed record is newer.
    """
    cache = MyUWMemcachedCache()
    response = cache.getCache("sws", url)
    if response:
        date_str = response.getheader("Date")
        if date_str:
            cached_dt = localtime(parse(date_str))
            if new_value_dt <= cached_dt:
                return

    new_response = CachedHTTPResponse(data=json.dumps(new_value), status=200)
    cache.updateCache("sws", url, new_response)
