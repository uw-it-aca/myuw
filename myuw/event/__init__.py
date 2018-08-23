from myuw.util.cache_implementation import MyUWMemcachedCache


myuwcache = MyUWMemcachedCache()


def update_sws_entry_in_cache(url, new_value, time_stamp):
    myuwcache.update_cache("sws", url, new_value)
