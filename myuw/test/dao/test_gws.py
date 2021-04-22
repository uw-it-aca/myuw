# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.gws import (
    is_clinician, is_seattle_student, is_bothell_student, is_tacoma_student,
    is_grad_and_prof_student, is_grad_student, is_undergrad_student,
    is_student, is_pce_student, is_grad_c2, is_undergrad_c2,
    is_student_employee, is_staff_employee, is_regular_employee,
    is_alum_asso, is_applicant, no_major_affiliations, get_groups,
    is_effective_member, in_myuw_test_access_group, in_fyp_group,
    in_au_xfer_group, in_wi_xfer_group, in_hxtoolkit_group)
from myuw.test import fdao_gws_override, get_request_with_user


@fdao_gws_override
class TestPwsDao(TestCase):

    def test_get_groups(self):
        req = get_request_with_user('jinter')
        self.assertFalse(hasattr(req, "myuwgwsgroups"))
        groups = get_groups(req)
        self.assertIsNotNone(req.myuwgwsgroups)
        self.assertTrue(is_grad_student(req))
        self.assertTrue(is_student_employee(req))
        self.assertTrue(is_grad_c2(req))

    def test_is_types(self):
        req = get_request_with_user('javerage')
        self.assertTrue(is_seattle_student(req))
        self.assertTrue(is_undergrad_student(req))
        self.assertTrue(is_pce_student(req))
        self.assertTrue(is_student_employee(req))
        self.assertFalse(is_bothell_student(req))
        self.assertFalse(is_tacoma_student(req))
        self.assertFalse(is_grad_and_prof_student(req))
        self.assertFalse(is_grad_student(req))
        self.assertFalse(is_staff_employee(req))

        req = get_request_with_user('jnew')
        self.assertTrue(in_fyp_group(req))

        req = get_request_with_user('javg001')
        self.assertTrue(in_au_xfer_group(req))

        req = get_request_with_user('javg002')
        self.assertTrue(in_wi_xfer_group(req))

        req = get_request_with_user('javg003')
        self.assertTrue(in_au_xfer_group(req))
        self.assertTrue(in_wi_xfer_group(req))
        self.assertFalse(in_fyp_group(req))

        req = get_request_with_user('jbothell')
        self.assertFalse(is_student_employee(req))
        self.assertTrue(is_bothell_student(req))
        self.assertTrue(is_undergrad_student(req))

        req = get_request_with_user('eight')
        self.assertTrue(is_student_employee(req))
        self.assertTrue(is_tacoma_student(req))
        self.assertTrue(is_undergrad_student(req))
        self.assertFalse(is_regular_employee(req))

        req = get_request_with_user('seagrad')
        self.assertTrue(is_grad_and_prof_student(req))
        self.assertTrue(is_grad_student(req))
        self.assertTrue(is_staff_employee(req))
        self.assertTrue(is_regular_employee(req))

        req = get_request_with_user('curgrad')
        self.assertTrue(is_grad_and_prof_student(req))
        self.assertFalse(is_grad_student(req))

        req = get_request_with_user('staff')
        self.assertTrue(is_regular_employee(req))
        self.assertTrue(is_staff_employee(req))
        self.assertTrue(is_clinician(req))
        self.assertTrue(in_hxtoolkit_group(req))

        req = get_request_with_user('bill')
        self.assertTrue(is_clinician(req))
        self.assertFalse(in_hxtoolkit_group(req))

        req = get_request_with_user('nobody')
        self.assertTrue(no_major_affiliations(req))

        req = get_request_with_user('no_entity')
        self.assertRaises(DataFailureException,
                          no_major_affiliations, req)

        req = get_request_with_user('jalum')
        self.assertTrue(is_alum_asso(req))

    def test_is_pce(self):
        req = get_request_with_user('jpce')
        self.assertTrue(is_undergrad_c2(req))
        self.assertFalse(is_grad_c2(req))

        req = get_request_with_user('jinter')
        self.assertTrue(is_grad_c2(req))
        self.assertTrue(is_seattle_student(req))
        self.assertTrue(is_grad_student(req))
        self.assertTrue(is_pce_student(req))
        self.assertTrue(is_student_employee(req))

    def test_is_effective_member(self):
        req = get_request_with_user('bill')
        self.assertTrue(
            is_effective_member(req, 'u_astratst_myuw_test-support-admin'))

    def test_in_myuw_test_access_group(self):
        self.assertTrue(in_myuw_test_access_group(
            get_request_with_user("anyone")))

        with self.settings(
                MYUW_TEST_ACCESS_GROUP='u_astratst_myuw_test-support-admin'):
            self.assertTrue(in_myuw_test_access_group(
                get_request_with_user("javerage")))
            self.assertFalse(in_myuw_test_access_group(
                get_request_with_user("eight")))
