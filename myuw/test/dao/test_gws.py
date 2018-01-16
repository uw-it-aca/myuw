from django.test import TestCase
from restclients_core.exceptions import DataFailureException, InvalidNetID
from myuw.dao.gws import get_groups, is_seattle_student,\
    is_bothell_student, is_tacoma_student, is_current_graduate_student,\
    is_grad_student, is_undergrad_student, is_student, is_pce_student,\
    is_student_employee, is_faculty, is_employee, is_staff_employee,\
    is_applicant, is_grad_c2, is_undergrad_c2
from myuw.test import fdao_gws_override, get_request_with_user


@fdao_gws_override
class TestPwsDao(TestCase):

    def test_get_groups(self):
        get_request_with_user('javerage')
        grs = get_groups('javerage')
        self.assertEquals(len(grs), 5)
        self.assertTrue(is_seattle_student())
        self.assertTrue(is_undergrad_student())
        self.assertTrue(is_pce_student())
        self.assertTrue(is_student_employee())
        self.assertTrue(is_employee())
        self.assertFalse(is_bothell_student())
        self.assertFalse(is_tacoma_student())
        self.assertFalse(is_current_graduate_student())
        self.assertFalse(is_grad_student())
        self.assertFalse(is_staff_employee())
        self.assertFalse(is_faculty())

        get_request_with_user('jpce')
        grs = get_groups('jpce')
        self.assertTrue(is_undergrad_c2())

        get_request_with_user('jinter')
        grs = get_groups('jinter')
        self.assertTrue(is_grad_c2())
