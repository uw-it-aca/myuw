# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import sys
import threading
from django.db import connection
from django.conf import settings
from userservice.user import UserServiceMiddleware


class Thread(threading.Thread):
    parent = None
    _use_thread = False

    def __init__(self, *args, **kwargs):
        if getattr(settings, "MYUW_PREFETCH_THREADING", True):
            self.parent = threading.currentThread()
            self._use_thread = True

        super().__init__(*args, **kwargs)

    def start(self):
        if self._use_thread:
            super().start()
        else:
            self.run()

    def join(self):
        if self._use_thread:
            return super().join()
        return True

    def close_connection(self):
        if self._use_thread:
            if not connection.in_atomic_block:
                connection.close()


class PrefetchThread(Thread):
    method = None
    request = None

    def run(self):
        if self.method is None or self.request is None:
            return

        try:
            UserServiceMiddleware().process_request(self.request)
            self.method(self.request)
        except Exception as ex:
            # We need to be sure that any prefetch errors don't crash the page!
            pass

        self.close_connection()


class ThreadWithResponse(Thread):
    def run(self):
        self.response = None
        self.exception = None

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

        self.close_connection()
