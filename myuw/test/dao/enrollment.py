from django.test import TestCase
from unittest import skip
from myuw.dao.enrollment import (get_minors_for_terms, get_majors_for_terms,
                                 _get_all_enrollments,
                                 _get_current_quarter_enrollment)
from myuw.dao.term import get_current_and_next_quarters, get_current_quarter
from myuw.test import (get_user, get_user_pass, fdao_pws_override,
                       get_request_with_user, get_request_with_date,
                       fdao_sws_override, fdao_uwnetid_override)

class TestEnrollment(TestCase):

    def set_user(self, user):
        get_user(user)
        self.client.login(username=user,
                          password=get_user_pass(user))

    def test_get_enrollment_quarter(self):
        request = get_request_with_date("2013-04-15")
        # javerage's regid
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        enrollment = _get_current_quarter_enrollment(request, regid)

    def test_get_all_enrollment(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        request = get_request_with_date("2013-04-15")
        terms = get_current_and_next_quarters(request, 4)
        enrollments = _get_all_enrollments(regid)
        self.assertEquals(len(enrollments), 4)

        for term in terms:
            self.assertIn(term, enrollments)

        spring_enrollment = enrollments[terms[0]]

        self.assertEquals(len(spring_enrollment.majors), 1)
        self.assertEquals(len(spring_enrollment.minors), 1)

    def test_get_majors_for_terms(self):
        regid = "12345678901234567890123456789012"
        request = get_request_with_date("2013-04-15")
        terms = get_current_and_next_quarters(request, 4)
        enrollments = _get_all_enrollments(regid)

        majors = get_majors_for_terms(terms, enrollments)

        self.assertEquals(len(majors[0]['majors']), 2)
        self.assertEquals(len(majors[1]['majors']), 3)
        self.assertEquals(len(majors[2]['majors']), 2)

    def test_get_minors_for_terms(self):
        regid = "FE36CCB8F66711D5BE060004AC494FCD"
        request = get_request_with_date("2013-04-15")
        terms = get_current_and_next_quarters(request, 4)
        enrollments = _get_all_enrollments(regid)

        minors = get_minors_for_terms(terms, enrollments)

        self.assertEquals(len(minors[0]['minors']), 1)
        self.assertEquals(len(minors[1]['minors']), 2)
        self.assertEquals(len(minors[2]['minors']), 1)
