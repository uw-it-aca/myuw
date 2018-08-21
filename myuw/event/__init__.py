from uw_sws.dao import SWS_DAO
from myuw.util.cache_implementation import MyUWMemcachedCache


myuwcache = MyUWMemcachedCache()
SWS_SERVICE_NAME = SWS_DAO().service_name


def update_cached_sws_entry(url, new_value):
    myuwcache.update_cache(SWS_SERVICE_NAME, url, new_value)
