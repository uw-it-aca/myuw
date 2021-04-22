# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from myuw.views.error import (
    not_instructor_error, data_not_found, no_access, data_error,
    disabled_action_error, invalid_future_term, invalid_input_data,
    invalid_method, not_instructor_error, unknown_uwnetid,
    blocked_uwnetid, pws_error_404)
from myuw.test.api import MyuwApiTest


class TestViewsError(MyuwApiTest):

    def test_data_not_found(self):
        response = data_not_found()
        self.assertEquals(response.content, b'Data not found')
        self.assertEquals(response.status_code, 404)

    def test_not_instructor_error(self):
        response = not_instructor_error()
        self.assertEquals(response.content,
                          b'Access Forbidden to Non Instructor')
        self.assertEquals(response.status_code, 403)

    def test_blocked_uwnetid(self):
        response = blocked_uwnetid()
        self.assertEquals(
            response.content,
            (b'<p>MyUW encountered a problem with your uwnetid, '
             b'please contact the <a href="https://itconnect.uw.edu/'
             b'it-connect-home/question/">UW-IT Service Center</a>.</p>'))
        self.assertEquals(response.status_code, 403)

    def pws_error_404(self):
        response = pws_error_404()
        self.assertEquals(
            response.content,
            (b'<p>MyUW cannot find data for this user account in the Person '
             b'Registry services. Please contact the <a href="https://'
             b'itconnect.uw.edu/it-connect-home/question/">UW-IT Service '
             b'Center</a>.</p>'))
        self.assertEquals(response.status_code, 403)

    def test_unknown_uwnetid(self):
        response = unknown_uwnetid()
        self.assertEquals(
            response.content,
            (b'<p>MyUW cannot find data for this user account in the Person '
             b'Registry services. If you have just created your UW NetID, '
             b'please try signing in to MyUW again in one hour.</p>'))
        self.assertEquals(response.status_code, 403)

    def test_disabled_action_error(self):
        response = disabled_action_error()
        self.assertEquals(response.content,
                          b'Action Disabled while overriding users')
        self.assertEquals(response.status_code, 403)

    def test_no_access(self):
        response = no_access()
        self.assertEquals(
            response.content,
            (b'<p>This is a test environment of MyUW, '
             b'its access is limited to specific people. To request access, '
             b'please contact the <a href="https://itconnect.uw.edu/'
             b'it-connect-home/question/">UW-IT Service Center</a>.</p>'))
        self.assertEquals(response.status_code, 403)

    def test_not_instructor_error(self):
        response = not_instructor_error()
        self.assertEquals(response.content,
                          b'Access Forbidden to Non Instructor')
        self.assertEquals(response.status_code, 403)

    def test_invalid_input_data(self):
        response = invalid_input_data()
        self.assertEquals(response.content, b'Invalid post data content')
        self.assertEquals(response.status_code, 400)

    def test_invalid_method(self):
        response = invalid_method()
        self.assertEquals(response.content, b'Method not allowed')
        self.assertEquals(response.status_code, 405)

    def test_invalid_future_term(self):
        response = invalid_future_term("2013,spring")
        self.assertEquals(response.content,
                          b'Invalid requested future term 2013,spring')
        self.assertEquals(response.status_code, 410)

    def test_data_error(self):
        response = data_error()
        self.assertEquals(response.content,
                          b'Data not available due to an error')
        self.assertEquals(response.status_code, 543)
