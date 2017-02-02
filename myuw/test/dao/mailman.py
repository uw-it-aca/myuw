from django.test import TestCase
from restclients.exceptions import DataFailureException
from restclients.sws.section import get_section_by_label
from myuw.dao.mailman import get_list_json,\
    get_instructor_term_list, get_section_secondary_combined_list,\
    get_single_course_list, get_single_section_list, get_section_id,\
    get_all_secondary_section_lists, get_section_email_lists
from myuw.test import fdao_sws_override, fdao_mailman_override, get_request,\
    get_request_with_user


@fdao_mailman_override
@fdao_sws_override
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

        self.assertRaises(DataFailureException,
                          get_single_course_list,
                          'T ARTS', '110', 'A', 'spring', 2016)

    def test_get_single_section_list(self):
        section = get_section_by_label('2013,spring,PHYS,121/A')
        url = "https://mailman.u.washington.edu/mailman/admin/phys121a_sp13"
        self.assertEqual(
            get_single_section_list(section),
            {"list_exists": True,
             "list_address": "phys121a_sp13",
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

    def test_secondary_combined_list(self):
        primary_section = get_section_by_label('2013,spring,PHYS,121/A')
        blist = get_section_secondary_combined_list(primary_section)
        self.assertEqual(blist["list_address"], 'multi_phys121a_sp13')
        self.assertTrue(blist["list_exists"])

    def test_get_section_email_lists(self):
        ret_json = get_section_email_lists(
            get_section_by_label('2013,spring,PHYS,121/A'), True)
        self.assertEqual(ret_json["course_abbr"], "PHYS")
        self.assertEqual(ret_json["course_number"], "121")
        self.assertEqual(ret_json["section_id"], "A")
        self.assertTrue(ret_json["is_primary"])
        self.assertEqual(ret_json["section_list"]["list_address"],
                         'phys121a_sp13')
        self.assertTrue(ret_json["section_list"]["list_exists"])

        self.assertTrue(ret_json["has_multi_secondaries"])
        self.assertEqual(len(ret_json['secondary_lists']), 21)
        self.assertEqual(ret_json["secondary_lists"][0]["list_address"],
                         'phys121aa_sp13')
        self.assertEqual(ret_json["secondary_lists"][20]["list_address"],
                         'phys121av_sp13')

        self.assertEqual(ret_json["secondary_combined_list"]["list_address"],
                         'multi_phys121a_sp13')
        self.assertTrue(ret_json["secondary_combined_list"]["list_exists"])

        ret_json = get_section_email_lists(
            get_section_by_label('2013,spring,ESS,102/A'), True)
        self.assertFalse(ret_json["section_list"]["list_exists"])
        self.assertEqual(len(ret_json["secondary_lists"]), 1)
        self.assertFalse(ret_json["has_multi_secondaries"])

        ret_json = get_section_email_lists(
            get_section_by_label('2013,spring,TRAIN,101/A'), True)
        self.assertTrue(ret_json["section_list"]["list_exists"])
        self.assertIsNone(ret_json["secondary_lists"])
