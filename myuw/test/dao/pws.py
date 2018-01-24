from django.test import TestCase
from restclients_core.exceptions import DataFailureException, InvalidNetID
from myuw.dao.pws import pws, get_display_name_of_current_user, is_employee,\
    is_student, is_bothell_employee, is_seattle_employee, is_tacoma_employee,\
    get_person_of_current_user
from myuw.test import fdao_pws_override, get_request_with_user


@fdao_pws_override
class TestPwsDao(TestCase):

    def test_not_in_pws_netid(self):
        self.assertRaises(InvalidNetID,
                          pws.get_person_by_netid,
                          "thisisnotarealnetid")

    def test_pws_err(self):
        self.assertRaises(DataFailureException,
                          pws.get_person_by_netid,
                          "nobody")

    def test_get_person_of_current_user(self):
        req = get_request_with_user('javerage')
        self.assertFalse(hasattr(req, "myuwpwsperson"))
        person = get_person_of_current_user(req)
        self.assertIsNotNone(req.myuwpwsperson)

    def test_display_name(self):
        req = get_request_with_user('javerage')
        self.assertEqual(get_display_name_of_current_user(req),
                         'J. Average Student')

    def test_is_student(self):
        req = get_request_with_user('javerage')
        self.assertTrue(is_student(req))

    def test_instructor_seattle_campus(self):
        req = get_request_with_user('bill')
        self.assertTrue(is_employee(req))
        self.assertTrue(is_seattle_employee(req))

    def test_instructor_bothell_campus(self):
        req = get_request_with_user('billbot')
        self.assertTrue(is_employee(req))
        self.assertTrue(is_bothell_employee(req))

    def test_instructor_tacoma_campus(self):
        req = get_request_with_user('billtac')
        self.assertTrue(is_employee(req))
        self.assertTrue(is_tacoma_employee(req))
