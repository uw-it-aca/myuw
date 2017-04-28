from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.term import get_current_quarter,\
    get_next_quarter, get_term_before, get_term_after
from myuw.dao.enrollment import get_enrollment_of_aterm,\
    get_enrollments_of_terms, get_current_quarter_enrollment
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestDaoEnrollment(TestCase):

    def test_get_enrollment_of_aterm(self):
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

    def test_get_enrollment_of_aterm(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-10"))
        term = get_next_quarter(req)
        enrollment = get_enrollment_of_aterm(term)
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
        self.assertEqual(len(enrollments), 1)
        self.assertTrue(t1 in enrollments)
        self.assertFalse(t2 in enrollments)
        self.assertFalse(t2 in enrollments)
        enrollment = get_enrollment_of_aterm(t1)
        self.assertEqual(len(enrollment.majors), 1)
        self.assertEqual(enrollment.majors[0].campus, "Bothell")

        req = get_request_with_user('eight',
                                    get_request_with_date("2013-04-01"))
        enrollments = get_enrollments_of_terms(terms)
        self.assertEqual(len(enrollments), 1)
        self.assertTrue(t1 in enrollments)
        self.assertFalse(t2 in enrollments)
        self.assertFalse(t2 in enrollments)
        enrollment = get_enrollment_of_aterm(t1)
        self.assertEqual(len(enrollment.majors), 2)
        self.assertEqual(enrollment.majors[0].campus, "Tacoma")
