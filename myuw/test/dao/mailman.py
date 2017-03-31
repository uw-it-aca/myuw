from django.test import TestCase
from django.core import mail
from restclients.exceptions import DataFailureException
from restclients.sws.section import get_section_by_label
from myuw.dao.mailman import get_list_json,\
    get_instructor_term_list, get_section_secondary_combined_list,\
    get_single_course_list, get_single_section_list, get_section_id,\
    get_all_secondary_section_lists, get_section_email_lists,\
    get_section_label, get_course_email_lists, request_mailman_lists,\
    get_message_body, _get_single_line, _get_quarter_code
from myuw.test import fdao_sws_override, fdao_mailman_override, get_request,\
    get_request_with_user, email_backend_override


@fdao_mailman_override
@fdao_sws_override
@email_backend_override
class TestMailmanDao(TestCase):
    def setUp(self):
        get_request()

    def test_get_list_json(self):
        url = "https://mailman.u.washington.edu/mailman/admin/bbio180a_su13"
        self.assertEqual(
            get_list_json(True, "bbio180a_su13"),
            {"list_exists": True,
             "list_address": "bbio180a_su13",
             "list_admin_url": url})

    def test_get_section_id(self):
        self.assertEqual(
            get_section_id("/student/v5/course/2013,spring,PHYS,121/AA.json"),
            "AA")

    def test_get_instructor_term_list(self):
        url = "https://mailman.u.washington.edu/mailman/admin/bill_au13"
        self.assertEqual(
            get_instructor_term_list('bill', 'autumn', 2013),
            {"list_exists": True,
             "list_address": "bill_au13",
             "list_admin_url": url})

    def test_get_single_course_list(self):
        list_data = get_single_course_list('B BIO', 180, 'A', 'summer', 2013)
        self.assertEqual(
            list_data["list_admin_url"],
            "https://mailman.u.washington.edu/mailman/admin/bbio180a_su13")
        self.assertEqual(
            list_data["list_address"], 'bbio180a_su13')
        self.assertTrue(list_data["list_exists"])
        self.assertEqual(list_data["section_id"], "A")

        self.assertRaises(DataFailureException,
                          get_single_course_list,
                          'T ARTS', '110', 'A', 'spring', 2016)
        list_data = get_single_course_list('ESS', '102', 'A', 'spring', 2013)
        self.assertFalse(list_data["list_exists"])
        self.assertEqual(list_data["section_label"], "2013,spring,ESS,102/A")
        self.assertEqual(list_data["section_id"], "A")

    def test_get_single_section_list(self):
        section = get_section_by_label('2013,spring,PHYS,121/A')
        url = "https://mailman.u.washington.edu/mailman/admin/phys121a_sp13"
        self.assertEqual(
            get_single_section_list(section),
            {"list_exists": True,
             "list_address": "phys121a_sp13",
             "section_id": 'A',
             'section_label': u'2013,spring,PHYS,121/A',
             "list_admin_url": url})

        list_data = get_single_section_list(
            get_section_by_label('2013,summer,B BIO,180/A'))
        self.assertEqual(list_data["list_address"], 'bbio180a_su13')
        self.assertTrue(list_data["list_exists"])

        list_data = get_single_section_list(
            get_section_by_label('2013,summer,B BIO,180/AA'))
        self.assertEqual(list_data["list_address"], 'bbio180aa_su13')
        self.assertTrue(list_data["list_exists"])

        list_data = get_single_section_list(
            get_section_by_label('2013,spring,T ARTS,110/A'))
        self.assertEqual(list_data["list_address"], 'tarts110a_sp13')
        self.assertTrue(list_data["list_exists"])

    def test_get_all_secondary_section_lists(self):
        primary_section = get_section_by_label('2013,spring,PHYS,121/A')
        sec_lists = get_all_secondary_section_lists(primary_section)
        self.assertEqual(len(sec_lists), 21)
        list1 = sec_lists[0]
        self.assertEqual(list1["list_address"], 'phys121aa_sp13')
        self.assertTrue(list1["list_exists"])
        list21 = sec_lists[20]
        self.assertEqual(list21["list_address"], 'phys121av_sp13')
        self.assertTrue(list21["list_exists"])

        primary_section = get_section_by_label('2013,spring,TCSS,305/A')
        sec_lists = get_all_secondary_section_lists(primary_section)
        self.assertEqual(len(sec_lists), 0)

    def test_secondary_combined_list(self):
        primary_section = get_section_by_label('2013,spring,PHYS,121/A')
        blist = get_section_secondary_combined_list(primary_section)
        self.assertEqual(blist["list_address"], 'multi_phys121a_sp13')
        self.assertTrue(blist["list_exists"])

    def test_get_course_email_lists(self):
        ret_json = get_course_email_lists(
            2013, 'spring', 'PHYS', '123', 'AA', True)
        self.assertEqual(ret_json["course_abbr"], "PHYS")
        self.assertEqual(ret_json["course_number"], "123")
        self.assertEqual(ret_json["section_id"], "AA")
        self.assertFalse(ret_json["is_primary"])
        self.assertEqual(ret_json["section_list"]["list_address"],
                         'phys123aa_sp13')
        self.assertFalse(ret_json["section_list"]["list_exists"])
        self.assertFalse(ret_json["has_multiple_sections"])
        self.assertEqual(ret_json["total_course_wo_list"], 1)
        self.assertTrue(ret_json["no_secondary_section"])

    def test_get_section_email_lists(self):
        ret_json = get_section_email_lists(
            get_section_by_label('2013,spring,PHYS,122/A'), True)
        self.assertEqual(ret_json["course_abbr"], "PHYS")
        self.assertEqual(ret_json["course_number"], "122")
        self.assertEqual(ret_json["section_id"], "A")
        self.assertTrue(ret_json["is_primary"])
        self.assertEqual(ret_json["section_list"]["list_address"],
                         'phys122a_sp13')
        self.assertFalse(ret_json["section_list"]["list_exists"])
        self.assertTrue(ret_json["has_multiple_sections"])
        self.assertEqual(ret_json["total_course_wo_list"], 10)
        self.assertEqual(len(ret_json['secondary_section_lists']), 11)
        self.assertEqual(
            ret_json["secondary_section_lists"][0]["list_address"],
            'phys122aa_sp13')
        self.assertEqual(
            ret_json["secondary_section_lists"][10]["list_address"],
            'phys122at_sp13')
        self.assertEqual(ret_json["secondary_combined_list"]["list_address"],
                         'multi_phys122a_sp13')
        self.assertFalse(ret_json["secondary_combined_list"]["list_exists"])

        ret_json = get_section_email_lists(
            get_section_by_label('2013,spring,ESS,102/A'), True)
        self.assertFalse(ret_json["section_list"]["list_exists"])
        self.assertEqual(ret_json["section_list"]["section_label"],
                         '2013,spring,ESS,102/A')
        self.assertEqual(len(ret_json["secondary_section_lists"]), 1)
        self.assertTrue(ret_json["has_multiple_sections"])

        ret_json = get_section_email_lists(
            get_section_by_label('2013,spring,TRAIN,101/A'), True)
        self.assertTrue(ret_json["section_list"]["list_exists"])
        self.assertTrue(ret_json["no_secondary_section"])

    def test_get_section_label(self):
        self.assertEqual(get_section_label('T ARTS', '110', 'A',
                                           'spring', 2016),
                         '2016,spring,T ARTS,110/A')
        self.assertEqual(get_section_label('ESS', '102', 'A',
                                           'spring', 2013),
                         '2013,spring,ESS,102/A')

    def test__get_quarter_code(self):
        self.assertEqual(_get_quarter_code('winter'), 1)
        self.assertEqual(_get_quarter_code('spring'), 2)
        self.assertEqual(_get_quarter_code("summer"), 3)
        self.assertEqual(_get_quarter_code("autumn"), 4)

    def test__get_single_line(self):
        self.assertEqual(
            _get_single_line(get_section_by_label(
                    '2013,spring,PHYS,122/A')),
            u'phys122a_sp13 2 2013 17983\n')

    def test_get_message_body(self):
        body, num1 = get_message_body('billsea',
                                      ['2013,spring,PHYS,122/A',
                                       '2013,spring,PHYS,122/AA',
                                       '2013,spring,PHYS,122/AB',
                                       '2013,spring,PHYS,122/AH'])
        self.assertEqual(num1, 3)
        self.assertEqual(body,
                         (u'billsea\n' +
                          u'phys122a_sp13 2 2013 17983\n' +
                          u'phys122aa_sp13 2 2013 17984\n' +
                          u'phys122ab_sp13 2 2013 17985\n'))

    def test_request_mailman_lists(self):
        with self.settings(MAILMAN_COURSEREQUEST_RECIPIENT='dummy@uw.edu'):
            self.assertEquals(len(mail.outbox), 0)
            resp = request_mailman_lists('billsea',
                                         ['2013,spring,PHYS,122/A',
                                          '2013,spring,PHYS,122/AA',
                                          '2013,spring,PHYS,122/AB'])
            self.assertEqual(resp, {"request_sent": True,
                                    'total_lists_requested': 3})
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject,
                             'instructor Mailman request')
            self.assertEqual(mail.outbox[0].from_email, "billsea@uw.edu")
            self.assertEqual(mail.outbox[0].to, ['dummy@uw.edu'])
            self.assertTrue(len(mail.outbox[0].body) > 0)
