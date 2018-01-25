from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.gws import is_alumni, is_alum_asso, is_seattle_student,\
    is_bothell_student, is_tacoma_student, is_current_graduate_student,\
    is_grad_student, is_undergrad_student, is_student,\
    is_pce_student, is_grad_c2, is_undergrad_c2,\
    is_student_employee, is_staff_employee,\
    is_applicant, no_affiliation, get_groups, is_in_admin_group
from myuw.test import fdao_gws_override, get_request_with_user

GROUP_BACKEND = 'authz_group.authz_implementation.all_ok.AllOK'


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
        self.assertFalse(is_current_graduate_student(req))
        self.assertFalse(is_grad_student(req))
        self.assertFalse(is_staff_employee(req))

        req = get_request_with_user('jbothell')
        self.assertFalse(is_student_employee(req))
        self.assertTrue(is_bothell_student(req))
        self.assertTrue(is_undergrad_student(req))

        req = get_request_with_user('eight')
        self.assertTrue(is_student_employee(req))
        self.assertTrue(is_tacoma_student(req))
        self.assertTrue(is_undergrad_student(req))

        req = get_request_with_user('nobody')
        self.assertRaises(DataFailureException,
                          no_affiliation, req)

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

    def test_is_in_admin_group(self):
        with self.settings(AUTHZ_GROUP_BACKEND=GROUP_BACKEND):
            with self.settings(MYUW_ADMIN_GROUP='x'):
                self.assertTrue(is_in_admin_group('MYUW_ADMIN_GROUP'))

            with self.settings(USERSERVICE_ADMIN_GROUP='x'):
                self.assertTrue(is_in_admin_group('USERSERVICE_ADMIN_GROUP'))

            with self.settings(RESTCLIENTS_ADMIN_GROUP='x'):
                self.assertTrue(is_in_admin_group('RESTCLIENTS_ADMIN_GROUP'))
