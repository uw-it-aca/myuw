from django.test import TestCase
from myuw.dao.term import get_current_quarter, get_previous_quarter,\
    get_next_quarter, get_term_before, get_term_after
from myuw.dao.enrollment import get_current_quarter_enrollment,\
    get_enrollment_for_term, get_enrollments_of_terms,\
    get_prev_enrollments_with_open_sections
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestDaoEnrollment(TestCase):

    def test_get_current_quarter_enrollment(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-10-10"))
        enrollment = get_current_quarter_enrollment(req)
        self.assertIsNotNone(enrollment)
        self.assertEqual(len(enrollment.majors), 1)
        self.assertEqual(len(enrollment.minors), 1)

        req = get_request_with_user('none',
                                    get_request_with_date("2013-04-10"))
        enrollment = get_current_quarter_enrollment(req)
        self.assertIsNone(enrollment)

        req = get_request_with_user('jerror',
                                    get_request_with_date("2013-04-10"))
        enrollment = get_current_quarter_enrollment(req)
        self.assertIsNone(enrollment)

    def test_get_enrollment_for_term(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-10"))
        term = get_next_quarter(req)
        enrollment = get_enrollment_for_term(req, term)
        self.assertIsNotNone(enrollment)
        self.assertEqual(len(enrollment.majors), 1)
        self.assertEqual(len(enrollment.minors), 1)

        req = get_request_with_user('staff',
                                    get_request_with_date("2013-04-10"))
        t1 = get_current_quarter(req)
        enrollment = get_enrollment_for_term(req, t1)
        enrollment = get_current_quarter_enrollment(req)
        self.assertIsNone(enrollment)

        req = get_request_with_user('jbothell',
                                    get_request_with_date("2013-04-01"))
        t1 = get_current_quarter(req)
        enrollment = get_enrollment_for_term(req, t1)
        self.assertEqual(len(enrollment.majors), 1)
        self.assertEqual(enrollment.majors[0].campus, "Bothell")

        req = get_request_with_user('eight',
                                    get_request_with_date("2013-04-01"))
        t1 = get_current_quarter(req)
        enrollment = get_enrollment_for_term(req, t1)
        self.assertEqual(len(enrollment.majors), 2)
        self.assertEqual(enrollment.majors[0].campus, "Tacoma")

    def test_get_enrollments_of_terms(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-01"))
        terms = []
        t1 = get_current_quarter(req)
        t2 = get_next_quarter(req)
        t3 = get_term_after(t2)
        t4 = get_term_after(t3)
        terms.append(t1)
        terms.append(t2)
        terms.append(t3)
        terms.append(t4)
        enrollments = get_enrollments_of_terms(terms)
        self.assertEqual(len(enrollments), 4)

        self.assertTrue(t1 in enrollments)
        self.assertTrue(t2 in enrollments)
        self.assertTrue(t3 in enrollments)
        self.assertTrue(t4 in enrollments)
        self.assertFalse(get_term_before(t1) in enrollments)
        self.assertFalse(get_term_after(t4) in enrollments)

        enroll1 = enrollments.get(t1)
        self.assertEquals(len(enroll1.majors), 1)
        self.assertEquals(len(enroll1.minors), 1)

        enroll3 = enrollments.get(t3)
        self.assertTrue(enroll3.has_pending_major_change)
        self.assertEquals(len(enroll3.minors), 1)
        self.assertEquals(len(enroll3.minors), 1)
        self.assertTrue(enroll1.majors[0] != enroll3.majors[0])
        self.assertTrue(enroll1.minors[0] == enroll3.minors[0])

        enroll4 = enrollments.get(t4)
        self.assertTrue(enroll4.has_pending_major_change)
        self.assertEquals(len(enroll4.minors), 1)
        self.assertEquals(len(enroll4.minors), 1)
        self.assertTrue(enroll1.majors[0] != enroll4.majors[0])
        self.assertTrue(enroll3.majors[0] != enroll4.majors[0])
        self.assertTrue(enroll1.minors[0] != enroll4.minors[0])

        req = get_request_with_user('jbothell',
                                    get_request_with_date("2013-04-01"))
        enrollments = get_enrollments_of_terms(terms)
        self.assertEqual(len(enrollments), 1)
        self.assertTrue(t1 in enrollments)
        self.assertFalse(t2 in enrollments)
        self.assertFalse(t2 in enrollments)

        req = get_request_with_user('eight',
                                    get_request_with_date("2013-04-01"))
        enrollments = get_enrollments_of_terms(terms)
        self.assertEqual(len(enrollments), 1)
        self.assertTrue(t1 in enrollments)
        self.assertFalse(t2 in enrollments)
        self.assertFalse(t2 in enrollments)

    def test_get_prev_enrollments_with_open_sections(self):
        req = get_request_with_user('jpce',
                                    get_request_with_date("2013-04-29"))
        enrollements = get_prev_enrollments_with_open_sections(req, 2)
        self.assertEqual(len(enrollements), 1)

        term = get_previous_quarter(req)
        self.assertTrue(term in enrollements)
        sections = enrollements[term].off_term_sections
        self.assertEqual(len(sections), 2)
        self.assertIsNone(sections.get('3,winter,COM,201/A'))
        s1 = sections.get('2013,winter,COM,201/A')
        self.assertEqual(str(s1.end_date), '2013-04-29 00:00:00')
        s2 = sections.get('2013,winter,PSYCH,203/A')
        self.assertEqual(str(s2.end_date), '2013-04-30 00:00:00')

        req = get_request_with_user('jpce',
                                    get_request_with_date("2013-06-28"))
        enrollements = get_prev_enrollments_with_open_sections(req, 2)
        term = get_previous_quarter(req)
        self.assertTrue(term in enrollements)
        sections = enrollements[term].off_term_sections
        self.assertEqual(len(sections), 1)
        self.assertFalse('2013,spring,AAES,150/A' in sections)
        self.assertFalse('2013,spring,ACCTG,508/A' in sections)
        s1 = sections.get('2013,spring,CPROGRM,712/A')
        self.assertEqual(str(s1.end_date), '2013-06-28 00:00:00')
