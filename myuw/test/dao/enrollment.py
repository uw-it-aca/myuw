from django.test import TestCase
from myuw.dao.term import get_prev_num_terms, get_current_quarter,\
    get_previous_quarter, get_next_quarter, get_term_before
from myuw.dao.enrollment import get_enrollment_of_aterm,\
    get_prev_enrollments_with_open_sections, get_enrollments_of_terms,\
    get_current_quarter_enrollment
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestEnrollment(TestCase):

    def test_get_enrollment_of_aterm(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-10"))
        enrollement = get_current_quarter_enrollment(req)
        self.assertIsNotNone(enrollement)
        self.assertEqual(len(enrollement.off_term_sections), 0)

    def test_get_enrollments_of_terms(self):
        req = get_request_with_user('jpce',
                                    get_request_with_date("2013-07-10"))
        enrollements = get_enrollments_of_terms(get_prev_num_terms(req, 2))
        self.assertEqual(len(enrollements), 2)
        term = get_previous_quarter(req)
        self.assertTrue(term in enrollements)
        sections = enrollements[term].off_term_sections
        self.assertEqual(len(sections), 3)
        s1 = sections.get('2013,spring,AAES,150/A')
        self.assertEqual(str(s1.end_date), '2013-06-07 00:00:00')
        s2 = sections.get('2013,spring,ACCTG,508/A')
        self.assertEqual(str(s2.end_date), '2013-06-19 00:00:00')
        s3 = sections.get('2013,spring,CPROGRM,712/A')
        self.assertEqual(str(s3.end_date), '2013-06-28 00:00:00')
        self.assertTrue(get_previous_quarter(req) in enrollements)

        term = get_term_before(term)
        sections = enrollements[term].off_term_sections
        self.assertEqual(len(sections), 2)
        self.assertIsNone(sections.get('3,winter,COM,201/A'))
        s1 = sections.get('2013,winter,COM,201/A')
        self.assertEqual(str(s1.end_date), '2013-04-29 00:00:00')
        s2 = sections.get('2013,winter,PSYCH,203/A')
        self.assertEqual(str(s2.end_date), '2013-04-30 00:00:00')

        self.assertFalse(get_term_before(term) in enrollements)

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
