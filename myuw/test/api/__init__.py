# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
from unittest import skipIf
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TransactionTestCase, Client
from django.test.client import RequestFactory
from django.test.utils import override_settings
from userservice.user import UserServiceMiddleware
from myuw.test import (get_user, get_user_pass, fdao_uwnetid_override,
                       fdao_sws_override, fdao_subject_guide_override,
                       fdao_mylib_override, fdao_ias_override,
                       fdao_hfs_override, fdao_gws_override,
                       fdao_pws_override, fdao_grad_override,
                       fdao_bookstore_override, fdao_canvas_override,
                       fdao_mailman_override, fdao_upass_override)
from django.urls import NoReverseMatch

VALIDATE = "myuw.authorization.validate_netid"
OVERRIDE = "myuw.authorization.can_override_user"


def missing_url(name, kwargs=None):
    try:
        reverse(name, kwargs=kwargs)
    except NoReverseMatch as ex:
        print("NoReverseMatch: %s" % ex)
        return True

    return False


def require_url(url, message='myuw urls not configured', kwargs=None):
    if "FORCE_VIEW_TESTS" in os.environ:
        return skipIf(False, message)
    return skipIf(missing_url(url, kwargs), message)


Session = 'django.contrib.sessions.middleware.SessionMiddleware'
Common = 'django.middleware.common.CommonMiddleware'
CsrfView = 'django.middleware.csrf.CsrfViewMiddleware'
Auth = 'django.contrib.auth.middleware.AuthenticationMiddleware'
RemoteUser = 'django.contrib.auth.middleware.RemoteUserMiddleware'
Message = 'django.contrib.messages.middleware.MessageMiddleware'
XFrame = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
UserService = 'userservice.user.UserServiceMiddleware'
AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'
standard_test_override = override_settings(
    MIDDLEWARE=[Session,
                Common,
                CsrfView,
                Auth,
                RemoteUser,
                Message,
                XFrame,
                UserService],
    AUTHENTICATION_BACKENDS=[AUTH_BACKEND])


@standard_test_override
class MyuwApiTest(TransactionTestCase):

    def setUp(self):
        """
        By default enforce_csrf_checks is False
        """
        self.client = Client()
        self.request = RequestFactory().get("/")
        self.middleware = UserServiceMiddleware()

    def set_user(self, username):
        self.request.user = get_user(username)
        self.client.login(username=username,
                          password=get_user_pass(username))
        self.process_request()

    def process_request(self):
        self.request.session = self.client.session
        self.middleware.process_request(self.request)

    def set_date(self, date):
        session = self.client.session
        session['myuw_override_date'] = date
        session.save()

    def get_response_by_reverse(self, url_reverse, *args, **kwargs):
        url = reverse(url_reverse, *args, **kwargs)
        return self.client.get(url)

    def get_section(self, schedule_json_data, abbr, number, section_id):
        for section in schedule_json_data['sections']:
            if section['curriculum_abbr'] == abbr and\
                    section['course_number'] == number and\
                    section['section_id'] == section_id:
                return section
        self.fail('Did not find course %s %s %s' % (abbr, number, section_id))

    def set_userservice_override(self, username):
        with self.settings(DEBUG=False,
                           USERSERVICE_VALIDATION_MODULE=VALIDATE,
                           USERSERVICE_OVERRIDE_AUTH_MODULE=OVERRIDE):

            resp = self.client.post(reverse("userservice_override"),
                                    {"override_as": username})
            self.assertEquals(resp.status_code, 200)
            self.process_request()
