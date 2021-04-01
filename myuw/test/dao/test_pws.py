# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException, InvalidNetID
from myuw.dao.pws import (
    pws, get_display_name_of_current_user, is_employee, is_alumni, is_faculty,
    is_prior_employee, is_prior_student, is_retiree, is_student,
    is_bothell_employee, is_seattle_employee, is_tacoma_employee,
    get_person_of_current_user, get_regid_of_current_user,
    get_employee_id_of_current_user, get_student_number_of_current_user,
    get_student_system_key_of_current_user)
from myuw.test import fdao_pws_override, get_request_with_user, get_request


@fdao_pws_override
class TestPwsDao(TestCase):

    def test_no_entity_netid(self):
        self.assertRaises(InvalidNetID, pws.get_person_by_netid, "0")
        # netid max length is 128 now

        req = get_request_with_user('usernotinpws')
        self.assertRaises(DataFailureException,
                          get_person_of_current_user, req)

    def test_no_pws_person_netid(self):
        req = get_request_with_user('nobody')
        person = get_person_of_current_user(req)
        self.assertIsNotNone(req.myuw_pws_person)

    def test_get_regid_of_current_user(self):
        req = get_request_with_user('seagrad')
        self.assertEqual(get_regid_of_current_user(req),
                         u'10000000000000000000000000000002')
        self.assertTrue(is_employee(req))
        self.assertTrue(is_student(req))
        self.assertTrue(is_bothell_employee(req))

    def test_get_person_of_current_user(self):
        # test MUWM-4366 no user in request
        self.assertRaises(Exception, get_person_of_current_user, get_request())

        req = get_request_with_user('javerage')
        self.assertFalse(hasattr(req, "myuw_pws_person"))
        person = get_person_of_current_user(req)
        self.assertIsNotNone(req.myuw_pws_person)

    def test_display_name(self):
        req = get_request_with_user('javerage')
        self.assertEqual(get_display_name_of_current_user(req),
                         'J. Average Student')

    def test_is_alumni(self):
        req = get_request_with_user('jalum')
        self.assertTrue(is_alumni(req))
        req = get_request_with_user('faculty')
        self.assertTrue(is_alumni(req))

    def test_is_faculty(self):
        req = get_request_with_user('bill')
        self.assertTrue(is_faculty(req))
        self.assertTrue(is_prior_student(req))

    def test_is_retiree(self):
        req = get_request_with_user('retirestaff')
        self.assertTrue(is_retiree(req))
        self.assertTrue(is_alumni(req))
        self.assertTrue(is_prior_student(req))

    def test_is_prior_employee(self):
        req = get_request_with_user('jpce')
        self.assertTrue(is_prior_employee(req))

    def test_is_prior_student(self):
        req = get_request_with_user('faculty')
        self.assertTrue(is_prior_student(req))

    def test_is_student(self):
        req = get_request_with_user('javerage')
        self.assertTrue(is_student(req))
        self.assertEqual(get_student_system_key_of_current_user(req),
                         u'000083856')
        self.assertEqual(get_student_number_of_current_user(req),
                         u'1033334')

        req = get_request_with_user('botgrad')
        self.assertTrue(is_student(req))
        self.assertEqual(get_student_system_key_of_current_user(req),
                         u'001000003')
        self.assertEqual(get_student_number_of_current_user(req),
                         u'1000003')

    def test_instructor_seattle_campus(self):
        req = get_request_with_user('bill')
        self.assertEqual(get_employee_id_of_current_user(req),
                         u'123456782')
        self.assertTrue(is_employee(req))
        self.assertTrue(is_seattle_employee(req))

    def test_instructor_bothell_campus(self):
        req = get_request_with_user('billbot')
        self.assertTrue(is_alumni(req))
        self.assertTrue(is_employee(req))
        self.assertTrue(is_bothell_employee(req))
        self.assertTrue(is_prior_student(req))

    def test_instructor_tacoma_campus(self):
        req = get_request_with_user('billtac')
        self.assertTrue(is_employee(req))
        self.assertTrue(is_alumni(req))
        self.assertTrue(is_tacoma_employee(req))
