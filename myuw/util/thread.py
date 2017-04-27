import sys
import restclients.thread
from django.conf import settings
from userservice.user import UserServiceMiddleware


class Thread(restclients.thread.Thread):
    def __init__(self, *args, **kwargs):
        # Only enable threading if forced.  Using some cache backends
        # with sqlite doesn't work with threading.
        self._use_thread = getattr(settings, "MYUW_PREFETCH_THREADING", True)
        super(Thread, self).__init__(*args, **kwargs)

    def start(self):
        if self._use_thread:
            super(Thread, self).start()
        else:
            self.run()

    def join(self):
        if self._use_thread:
            return super(Thread, self).join()

        return True


class PrefetchThread(Thread):

    def run(self):
        try:
            UserServiceMiddleware().process_request(self.request)
            self.method(self.request)
        except Exception as ex:
            # We need to be sure that any prefetch errors don't crash the page!
            pass


class ThreadWithResponse(Thread):

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.response = None
        self.exception = None

    def run(self):
        try:
            if sys.version_info[0] == 2:
                if self._Thread__target is not None:
                    self.response = self._Thread__target(
                        *self._Thread__args, **self._Thread__kwargs)
            else:
                if self._target:
                    self.response = self._target(*self._args, **self._kwargs)
        except Exception as ex:
            self.exception = ex
