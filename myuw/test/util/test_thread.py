# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.contrib.sessions.middleware import SessionMiddleware
from myuw.util.thread import Thread, PrefetchThread, ThreadWithResponse


def request_prefetch(request):
    request.prefetched_data = '123456789ABCDEF'


def set_async_data():
    return '123456789ABCDEF'


def raise_async_exception():
    raise Exception('oops!')


class TestPrefetchThread(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        middleware = SessionMiddleware(self.request)
        middleware.process_request(self.request)
        self.request.session.save()

    def test_run(self):
        self.assertFalse(hasattr(self.request, 'prefetched_data'))

        thread = PrefetchThread()
        thread.method = request_prefetch
        thread.request = self.request
        thread.start()
        thread.join()

        self.assertEqual(self.request.prefetched_data, '123456789ABCDEF')


class TestThreadWithResponse(TestCase):
    def test_run(self):
        thread = ThreadWithResponse(target=set_async_data, args=())
        thread.start()
        thread.join()

        self.assertEqual(thread.response, '123456789ABCDEF')
        self.assertIsNone(thread.exception)

    def test_run_with_exception(self):
        thread = ThreadWithResponse(target=raise_async_exception, args=())
        thread.start()
        thread.join()

        self.assertEqual(str(thread.exception), 'oops!')
        self.assertIsNone(thread.response)
