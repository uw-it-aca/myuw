# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from myuw.test.api import MyuwApiTest
from blti import BLTI


def get_lti_request():
    request = RequestFactory().get("/lti")
    SessionMiddleware().process_request(request)
    request.session.save()

    kwargs = {'authorized_sections': ['2013-spring-ESS-102-A']}
    BLTI().set_session(request, **kwargs)
    return request


class MyuwLTITest(MyuwApiTest):
    pass
