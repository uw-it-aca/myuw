from uw_sws.dao import SWS_DAO
from myuw.util.cache_implementation import MyUWMemcachedCache


myuwcache = MyUWMemcachedCache()
SWS_SERVICE_NAME = SWS_DAO().service_name


def clear_cached_sws_entry(url):
    myuwcache.delete_cached_value(SWS_SERVICE_NAME, url)
