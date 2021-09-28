# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.test.utils import override_settings
from userservice.user import UserServiceMiddleware, UserService
from myuw.logger.session_log import (
    log_session, _get_affi, get_userids, _get_session_data, is_native)
from myuw.test import (
    get_request, get_request_with_user, set_override_user)


@override_settings(MIDDLEWARE_CLASSES=[UserServiceMiddleware])
class TestSessionLog(TestCase):
    def test_get_userids(self):
        req = get_request()
        self.assertEqual(get_userids(req), {'orig_netid': None,
                                            'acting_netid': None,
                                            "is_override": False})

        req = get_request_with_user('javerage')
        self.assertEqual(get_userids(req), {"orig_netid": "javerage",
                                            "acting_netid": "javerage",
                                            "is_override": False})
        log_session(req)

        set_override_user("bill", req)
        self.assertEqual(get_userids(req), {"acting_netid": "bill",
                                            "orig_netid": "javerage",
                                            "is_override": True})
        log_session(req)

    def test__get_affi(self):
        req = get_request_with_user('javerage')
        req.META['REMOTE_ADDR'] = '127.0.0.1'
        entry = _get_session_data(req)
        self.assertEquals(entry['ip'], '127.0.0.1')

        req.META['X-Forwarded-For'] = '127.0.0.2'
        entry = _get_session_data(req)
        self.assertEqual(entry['ip'], '127.0.0.2')

        req.META['HTTP_USER_AGENT'] = ' Safari/601.7.7 MyUW_Hybrid/1.0'
        entry = _get_session_data(req)
        self.assertTrue(entry['is_native'])

        entry = _get_affi(req)
        self.assertEqual(entry['class_level'], 'SENIOR')
        self.assertTrue(entry['ugrad'])
        self.assertTrue(entry['pce'])
        self.assertTrue(entry['student'])
        self.assertFalse(entry['employee'])
        self.assertFalse(entry['instructor'])
        self.assertFalse(entry['applicant'])
        self.assertFalse(entry['alumni'])
        self.assertFalse(entry['clinician'])
        self.assertFalse(entry['retired_staff'])
        self.assertFalse(entry['past_employee'])
        self.assertFalse(entry['past_stud'])
        self.assertTrue(entry['stud_employee'])
        self.assertTrue(entry['sea_stud'])
        self.assertFalse(entry['bot_stud'])
        self.assertFalse(entry['tac_stud'])
        self.assertTrue(entry['sea_emp'])
        self.assertFalse(entry['bot_emp'])
        self.assertFalse(entry['tac_emp'])
        self.assertTrue(entry['hxt_viewer'])

        req = get_request_with_user('jinter')
        entry = _get_affi(req)
        self.assertTrue(entry['intl_stud'])

        req = get_request_with_user('jalum')
        entry = _get_affi(req)
        self.assertTrue(entry['alumni'])
        self.assertTrue(entry['past_stud'])

    def test_is_native(self):
        req = get_request_with_user('javerage')
        self.assertFalse(is_native(req))
        req.META['HTTP_USER_AGENT'] = ' MyUW_Hybrid/1.0 (iPhone)'
        self.assertTrue(is_native(req))
