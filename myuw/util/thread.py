# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import sys
import threading
from django.db import connection
from userservice.user import UserServiceMiddleware


class Thread(threading.Thread):
    def close_db_connection(self):
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

        self.close_db_connection()


class ThreadWithResponse(Thread):
    response = None
    exception = None

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

        self.close_db_connection()
