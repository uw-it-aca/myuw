import time
import logging
from myuw.dao import get_netid_of_current_user


logger = logging.getLogger(__name__)


def log_response_time(func):
    def wrapper(*args, **kwargs):
        self = args[0]

        start = time.time()
        try:
            val = func(*args, **kwargs)
        except Exception:
            raise
        finally:
            module = self.__module__
            function = func.__name__

            is_view_class = True
            if module == "django.core.handlers.wsgi":
                is_view_class = False

            if is_view_class:
                arg_str = str(args[2:])
            else:
                arg_str = str(args[1:])

            kw_str = str(kwargs)
            end = time.time()

            try:
                netid = get_netid_of_current_user()
            except Exception as ex:
                netid = 'unknown_user'

            arg_str = arg_str.replace("#", "___")
            kw_str = kw_str.replace("#", "___")

            margs = (netid,
                     module,
                     function,
                     arg_str,
                     kw_str,
                     end-start)

            msg = "user# %s method# %s.%s args# %s kwargs# %s time# %s" % margs
            logger.info(msg)
        return val
    return wrapper
