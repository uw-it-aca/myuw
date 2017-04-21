from django.test import TestCase
from restclients_core.exceptions import DataFailureException, InvalidNetID
from uw_pws import PWS
from myuw.dao.pws import get_display_name_of_current_user,\
    is_student, get_campus_of_current_user
from myuw.test import fdao_pws_override, get_request_with_user


@fdao_pws_override
class TestPwsDao(TestCase):

    def test_not_in_pws_netid(self):
        self.assertRaises(InvalidNetID,
                          PWS().get_person_by_netid,
                          "thisisnotarealnetid")

    def test_pws_err(self):
        self.assertRaises(DataFailureException,
                          PWS().get_person_by_netid,
                          "nomockid")

    def test_display_name(self):
        get_request_with_user('javerage')
        name = get_display_name_of_current_user()
        self.assertEqual(name, 'J. Average Student')

    def test_is_student(self):
        get_request_with_user('javerage')
        self.assertTrue(is_student())

    def test_instructor_seattle_campus(self):
        get_request_with_user('bill')
        self.assertEquals(
            get_campus_of_current_user(), 'Seattle')

    def test_instructor_bothell_campus(self):
        get_request_with_user('billbot')
        self.assertEquals(
            get_campus_of_current_user(), 'Bothell')

    def test_instructor_tacoma_campus(self):
        get_request_with_user('billtac')
        self.assertEquals(
            get_campus_of_current_user(), 'Tacoma')
