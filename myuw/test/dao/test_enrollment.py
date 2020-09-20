from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.term import (
    get_current_quarter, get_previous_quarter,
    get_next_quarter, get_term_before, get_term_after)
from myuw.dao.enrollment import (
    get_current_quarter_enrollment, is_registered_current_quarter,
    get_enrollment_for_term, get_enrollments_of_terms,
    get_prev_enrollments_with_open_sections, is_ended,
    get_main_campus, enrollment_history, get_class_level)
from myuw.test import (
    fdao_sws_override, fdao_pws_override,
    get_request_with_date, get_request_with_user)


@fdao_pws_override
@fdao_sws_override
class TestDaoEnrollment(TestCase):

    def test_get_enrollment_for_term(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-10-10"))
        enrollment = get_current_quarter_enrollment(req)
        self.assertIsNotNone(enrollment)
        self.assertEqual(len(enrollment.majors), 1)
        self.assertEqual(len(enrollment.unf_pce_courses), 0)

        req = get_request_with_user('none',
                                    get_request_with_date("2013-04-10"))
        self.assertIsNone(get_current_quarter_enrollment(req))
        self.assertIsNone(get_class_level(req))

        req = get_request_with_user('jerror',
                                    get_request_with_date("2013-04-10"))
        self.assertIsNone(get_current_quarter_enrollment(req))

        req = get_request_with_user('staff',
                                    get_request_with_date("2013-04-10"))
        self.assertIsNone(get_current_quarter_enrollment(req))

    def get_enrollment(self, netid, req_date):
        req = get_request_with_user(netid,
                                    get_request_with_date(req_date))
        term = get_current_quarter(req)
        return get_enrollment_for_term(req, term)

    def test_multi_enrollments_for_a_course(self):
        enrollment = self.get_enrollment('seagrad', "2017-04-10")
        self.assertIsNotNone(enrollment)
        self.assertEqual(len(enrollment.majors), 1)

    def test_get_enrollment_for_term(self):
        enrollment = self.get_enrollment('staff', "2013-04-10")
        self.assertIsNone(enrollment)

        enrollment = self.get_enrollment('javerage', "2013-04-10")
        self.assertIsNotNone(enrollment)
        self.assertEqual(len(enrollment.majors), 1)
        self.assertEqual(len(enrollment.minors), 1)

        enrollment = self.get_enrollment('jbothell', "2013-04-01")
        self.assertEqual(len(enrollment.majors), 1)
        self.assertEqual(enrollment.majors[0].campus, "Bothell")

        enrollment = self.get_enrollment('eight', "2013-04-01")
        self.assertEqual(len(enrollment.majors), 2)
        self.assertEqual(enrollment.majors[0].campus, "Tacoma")

        enrollment = self.get_enrollment('jeos', "2013-10-10")
        self.assertEqual(len(enrollment.majors), 0)
        self.assertEqual(len(enrollment.minors), 0)
        self.assertTrue(enrollment.has_unfinished_pce_course())

        enrollment = self.get_enrollment('jpce', "2013-01-10")
        self.assertEqual(len(enrollment.majors), 1)
        self.assertEqual(len(enrollment.minors), 0)
        self.assertTrue(enrollment.has_unfinished_pce_course())

    def test_get_enrollments_of_terms(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-01"))
        self.assertEqual(get_class_level(req), "SENIOR")
        terms = []
        t1 = get_current_quarter(req)
        t2 = get_next_quarter(req)
        t3 = get_term_after(t2)
        terms.append(t1)
        terms.append(t2)
        terms.append(t3)
        enrollments = get_enrollments_of_terms(req, terms)
        self.assertEqual(len(enrollments), 3)

        self.assertTrue(t1 in enrollments)
        self.assertTrue(t2 in enrollments)
        self.assertTrue(t3 in enrollments)
        self.assertFalse(get_term_before(t1) in enrollments)
        self.assertFalse(get_term_after(t3) in enrollments)

        req = get_request_with_user('jbothell',
                                    get_request_with_date("2013-04-01"))
        enrollments = get_enrollments_of_terms(req, terms)
        self.assertEqual(len(enrollments), 2)
        self.assertTrue(t1 in enrollments)
        self.assertFalse(t2 in enrollments)
        self.assertTrue(t3 in enrollments)
        enrollment = get_enrollment_for_term(req, t1)
        self.assertEqual(len(enrollment.majors), 1)
        self.assertEqual(enrollment.majors[0].campus, "Bothell")

        req = get_request_with_user('eight',
                                    get_request_with_date("2013-04-01"))
        enrollments = get_enrollments_of_terms(req, terms)
        self.assertEqual(len(enrollments), 3)
        self.assertTrue(t1 in enrollments)
        self.assertTrue(t2 in enrollments)
        self.assertTrue(t3 in enrollments)
        enrollment = get_enrollment_for_term(req, t1)
        self.assertEqual(len(enrollment.majors), 2)
        self.assertEqual(enrollment.majors[0].campus, "Tacoma")

    def test_get_prev_enrollments_with_open_sections(self):
        req = get_request_with_user('jpce',
                                    get_request_with_date("2013-04-29"))
        enrollements = get_prev_enrollments_with_open_sections(req, 2)
        self.assertEqual(len(enrollements), 1)

        term = get_previous_quarter(req)
        self.assertTrue(term in enrollements)
        sections = enrollements[term].unf_pce_courses
        self.assertEqual(len(sections), 2)
        self.assertIsNone(sections.get('3,winter,COM,201/A'))
        s1 = sections.get('2013,winter,COM,201/A')
        self.assertFalse(is_ended(req, s1.end_date))
        self.assertEqual(str(s1.end_date), '2013-04-29')
        s2 = sections.get('2013,winter,PSYCH,203/A')
        self.assertEqual(str(s2.end_date), '2013-07-30')
        self.assertFalse(is_ended(req, s2.end_date))

        req = get_request_with_user('jpce',
                                    get_request_with_date("2013-06-28"))
        enrollements = get_prev_enrollments_with_open_sections(req, 2)
        term = get_previous_quarter(req)
        self.assertTrue(term in enrollements)
        sections = enrollements[term].unf_pce_courses
        self.assertEqual(len(sections), 2)
        self.assertFalse('2013,spring,AAES,150/A' in sections)
        self.assertTrue('2013,spring,CPROGRM,712/A' in sections)
        s1 = sections.get('2013,spring,CPROGRM,712/A')
        self.assertEqual(str(s1.end_date), '2013-06-30')

        self.assertFalse(is_ended(req, None))
        self.assertFalse(is_ended(req, ""))

    def test_is_registered_current_quarter(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-10"))
        self.assertTrue(is_registered_current_quarter(req))

        req = get_request_with_user('bill',
                                    get_request_with_date("2019-01-10"))
        self.assertFalse(is_registered_current_quarter(req))

    def test_get_main_campus(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-10"))
        campus = get_main_campus(req)
        self.assertEqual(len(campus), 1)
        self.assertEqual(campus[0], 'Seattle')

        req = get_request_with_user('jbothell',
                                    get_request_with_date("2013-04-10"))
        campus = get_main_campus(req)
        self.assertEqual(len(campus), 1)
        self.assertEqual(campus[0], 'Bothell')

        req = get_request_with_user('eight',
                                    get_request_with_date("2013-04-10"))
        campus = get_main_campus(req)
        self.assertEqual(len(campus), 1)
        self.assertEqual(campus[0], 'Tacoma')

        req = get_request_with_user('jpce',
                                    get_request_with_date("2013-04-10"))
        campus = get_main_campus(req)
        self.assertEqual(len(campus), 1)
        self.assertEqual(campus[0], 'Seattle')

        req = get_request_with_user('jeos',
                                    get_request_with_date("2013-04-10"))
        campus = get_main_campus(req)
        self.assertEqual(len(campus), 0)

        req = get_request_with_user('bill')
        campus = get_main_campus(req)
        self.assertEqual(len(campus), 0)

    def test_enrollment_history(self):
        req = get_request_with_user('javerage')
        history = enrollment_history(req)
        self.assertEqual(len(history), 4)
        self.assertIsNotNone(req.enrollment_history)
