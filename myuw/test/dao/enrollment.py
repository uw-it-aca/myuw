from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.term import get_current_quarter,\
    get_next_quarter, get_term_before, get_term_after,\
    get_current_and_next_quarters
from myuw.dao.enrollment import get_enrollment_for_term,\
    get_enrollments_of_terms, get_current_quarter_enrollment,\
    get_minors_for_terms, get_majors_for_terms, get_all_enrollments
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestDaoEnrollment(TestCase):

    def test_get_enrollment_for_term(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-10-10"))
        enrollment = get_current_quarter_enrollment(req)
        self.assertIsNotNone(enrollment)
        self.assertEqual(len(enrollment.majors), 2)
        self.assertEqual(len(enrollment.off_term_sections), 0)

        req = get_request_with_user('none',
                                    get_request_with_date("2013-04-10"))
        try:
            enrollment = get_current_quarter_enrollment(req)
            self.fail("should raise DataFailureException")
        except DataFailureException as ex:
            self.assertEqual(ex.status, 404)

        req = get_request_with_user('jerror',
                                    get_request_with_date("2013-04-10"))
        self.assertRaise(DataFailureException,
                         get_current_quarter_enrollment,
                         req)

        req = get_request_with_user('staff',
                                    get_request_with_date("2013-04-10"))
        enrollment = get_current_quarter_enrollment(req)
        self.assertEqual(len(enrollment.majors), 0)
        self.assertEqual(len(enrollment.minors), 0)

    def test_get_enrollment_for_term(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-10"))
        term = get_next_quarter(req)
        enrollment = get_enrollment_for_term(term)
        self.assertIsNotNone(enrollment)
        self.assertEqual(len(enrollment.majors), 1)
        self.assertEqual(len(enrollment.minors), 1)

    def test_get_enrollments_of_terms(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-01"))
        terms = []
        t1 = get_current_quarter(req)
        t2 = get_next_quarter(req)
        t3 = get_term_after(t2)
        terms.append(t1)
        terms.append(t2)
        terms.append(t3)
        enrollments = get_enrollments_of_terms(terms)
        self.assertEqual(len(enrollments), 3)

        self.assertTrue(t1 in enrollments)
        self.assertTrue(t2 in enrollments)
        self.assertTrue(t3 in enrollments)
        self.assertFalse(get_term_before(t1) in enrollments)
        self.assertFalse(get_term_after(t3) in enrollments)

        req = get_request_with_user('jbothell',
                                    get_request_with_date("2013-04-01"))
        enrollments = get_enrollments_of_terms(terms)
        self.assertEqual(len(enrollments), 3)
        self.assertTrue(t1 in enrollments)
        self.assertTrue(t2 in enrollments)
        self.assertTrue(t2 in enrollments)
        enrollment = get_enrollment_for_term(t1)
        self.assertEqual(len(enrollment.majors), 1)
        self.assertEqual(enrollment.majors[0].campus, "Bothell")

        req = get_request_with_user('eight',
                                    get_request_with_date("2013-04-01"))
        enrollments = get_enrollments_of_terms(terms)
        self.assertEqual(len(enrollments), 3)
        self.assertTrue(t1 in enrollments)
        self.assertTrue(t2 in enrollments)
        self.assertTrue(t2 in enrollments)
        enrollment = get_enrollment_for_term(t1)
        self.assertEqual(len(enrollment.majors), 2)
        self.assertEqual(enrollment.majors[0].campus, "Tacoma")

    def test_get_majors_for_terms(self):
        req = get_request_with_user('eight',
                                    get_request_with_date("2013-04-01"))
        terms = get_current_and_next_quarters(req, 4)
        enrollments = get_all_enrollments()

        majors = get_majors_for_terms(terms, enrollments)

        self.assertEquals(len(majors[0]['majors']), 2)
        self.assertEquals(len(majors[1]['majors']), 3)
        self.assertEquals(len(majors[2]['majors']), 2)

    def test_get_minors_for_terms(self):
        req = get_request_with_user('jbothell',
                                    get_request_with_date("2013-04-01"))
        terms = get_current_and_next_quarters(req, 4)
        enrollments = get_all_enrollments()

        minors = get_minors_for_terms(terms, enrollments)

        self.assertEquals(len(minors[0]['minors']), 1)
        self.assertEquals(len(minors[1]['minors']), 2)
        self.assertEquals(len(minors[2]['minors']), 1)
