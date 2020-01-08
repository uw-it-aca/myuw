from django.test import TestCase
from django.test.utils import override_settings
from myuw.logger.session_log import log_session, _get_affi,\
    get_userids, _get_session_data
from myuw.test import get_request_with_user

UserService = 'userservice.user.UserServiceMiddleware'


@override_settings(MIDDLEWARE_CLASSES=(UserService))
class TestSessionLog(TestCase):
    def test_mywm_2436(self):
        req = get_request_with_user('javerage')
        log_session(req)

    def test__get_affi(self):
        self.assertEqual(get_userids(), "")

        req = get_request_with_user('javerage')
        self.assertEqual(
            get_userids(),
            "{} {}".format(
                "orig_netid: javerage, acting_netid: javerage,",
                "is_override: False"))

        req.META['REMOTE_ADDR'] = '127.0.0.1'
        entry = _get_session_data(req)
        self.assertEquals(entry['ip'], '127.0.0.1')

        req.META['X-Forwarded-For'] = '127.0.0.2'
        entry = _get_session_data(req)
        self.assertEqual(entry['ip'], '127.0.0.2')

        entry = _get_affi(req)
        self.assertEqual(entry['class_level'], 'SENIOR')
        self.assertTrue(entry['is_ugrad'])
        self.assertTrue(entry['is_pce'])
        self.assertTrue(entry['is_student'])
        self.assertFalse(entry['is_employee'])
        self.assertFalse(entry['is_instructor'])
        self.assertFalse(entry['is_applicant'])
        self.assertFalse(entry['is_alumni'])
        self.assertFalse(entry['is_clinician'])
        self.assertFalse(entry['is_retired_staff'])
        self.assertFalse(entry['is_past_employee'])
        self.assertFalse(entry['is_past_stud'])
        self.assertTrue(entry['sea_stud'])
        self.assertFalse(entry['bot_stud'])
        self.assertFalse(entry['tac_stud'])
        self.assertTrue(entry['sea_emp'])
        self.assertFalse(entry['bot_emp'])
        self.assertFalse(entry['tac_emp'])
        self.assertFalse(entry['fyp'])
        self.assertFalse(entry['aut_transfer'])
        self.assertFalse(entry['win_transfer'])
        self.assertTrue(entry['hxt_viewer'])

        req = get_request_with_user('jinter')
        entry = _get_affi(req)
        self.assertTrue(entry['intl_stud'])

        req = get_request_with_user('jalum')
        entry = _get_affi(req)
        self.assertTrue(entry['is_alumni'])
        self.assertTrue(entry['is_past_stud'])
