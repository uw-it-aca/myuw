from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.term import get_current_quarter,\
    get_next_quarter, get_term_before, get_term_after,\
    get_current_and_next_quarters
from myuw.dao.enrollment import get_enrollment_for_term,\
    get_enrollments_of_terms, get_current_quarter_enrollment,\
    get_enrollments_of_terms
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request_with_user
from myuw.dao.student_profile import _get_degrees_for_terms


@fdao_pws_override
@fdao_sws_override
class TestStudentProfile(TestCase):
    def test_get_majors_for_terms(self):
        req = get_request_with_user('eight',
                                    get_request_with_date("2013-04-01"))
        terms = get_current_and_next_quarters(req, 4)
        enrollments = get_enrollments_of_terms(terms)

        majors = _get_degrees_for_terms(terms, enrollments, "majors")

        self.assertEquals(len(majors[0]['majors']), 2)
        self.assertEquals(len(majors[1]['majors']), 3)
        self.assertEquals(len(majors[2]['majors']), 2)

    def test_get_minors_for_terms(self):
        req = get_request_with_user('jbothell',
                                    get_request_with_date("2013-04-01"))
        terms = get_current_and_next_quarters(req, 4)
        enrollments = get_enrollments_of_terms(terms)

        minors = _get_degrees_for_terms(terms, enrollments, "minors")

        self.assertEquals(len(minors[0]['minors']), 1)
        self.assertEquals(len(minors[1]['minors']), 2)
        self.assertEquals(len(minors[2]['minors']), 1)

    def test_no_change(self):
        req = get_request_with_user('javg005',
                                    get_request_with_date("2013-04-01"))
        terms = get_current_and_next_quarters(req, 4)
        enrollments = get_enrollments_of_terms(terms)

        majors = _get_degrees_for_terms(terms, enrollments, "majors")
        minors = _get_degrees_for_terms(terms, enrollments, "minors")

        for major in majors:
            self.assertTrue(major['same_as_previous'])

        for minor in minors:
            self.assertTrue(minor['same_as_previous'])
