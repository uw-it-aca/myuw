# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from myuw.test.api import MyuwApiTest
from blti import BLTI
import mock


def get_lti_request():
    request = RequestFactory().get('/lti')
    get_response = mock.MagicMock()
    middleware = SessionMiddleware(get_response)
    response = middleware(request)
    request.session.save()

    kwargs = {'authorized_sections': ['2013-spring-ESS-102-A']}
    BLTI().set_session(request, **kwargs)
    return request


class MyuwLTITest(MyuwApiTest):
    pass
