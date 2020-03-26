from django.test import TestCase
from myuw.dao.notice_categorization import NOTICE_CATEGORIES


class TestNoticeCategories(TestCase):

    def test_categories(self):
        self.assertEqual(len(NOTICE_CATEGORIES.keys()), 75)

        categorization = NOTICE_CATEGORIES.get("studentalr_intlstucheckin")
        self.assertIsNotNone(categorization)
        self.assertEqual(categorization["myuw_category"], "Holds")
        self.assertTrue(categorization["critical"])
        self.assertEqual(len(categorization["location_tags"]), 2)

        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentalr_adminholds"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentalr_satprogblock"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentalr_preregnow"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentalr_hsimmunblock"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_hsimmunreqdatea"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_hsimmunreqdateb"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentgen_degreeappl"))

        categorization = NOTICE_CATEGORIES.get("studentdad_tuitdue")
        self.assertIsNotNone(categorization)
        self.assertEqual(len(categorization["location_tags"]), 3)

        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_estpd1regdate"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_intlsturegcutoffdate"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_intlstuftregcutoffdate"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_directdeposit"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_aidprioritydate"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_acceptrejectaward"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_disbursedatea"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_disbursedateb"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_loancounseling"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_loanpromissory"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_missingdocs"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_aidhold"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentgen_ferpa"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentgen_riaa"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentgen_acctbalance"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentgen_acctbaleonote"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentgen_intendedmajors"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentgen_majors"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_qtrbegin"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_lastdayregwochgfee"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_lastdayregchgfee"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_lastdaychgins"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_lastdaydropnorecord"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_lastdayauditopt"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_lastdaywoannualdrop"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_lastdaydrop"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_lastdayadd"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_lastdayannualdrop"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_lastdaychggradeopt"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_lastdaywithdraw"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentdad_commencement"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentgen_thankyouremark"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentgen_statussummary"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentgen_feespaid"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentclist_intlstucheckina"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentclist_intlstucheckinb"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentclist_advorientregdatea"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentclist_advorientregdateb"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentclist_advorientregdatec"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentclist_measlesa"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentclist_measlesb"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentclist_finaid"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentclist_emailservices"))

        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentclist_intendedmajor"))

        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentfoot_fiuts"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentfoot_summerreginfo"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "newstudentfoot_nextstep"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "ugapplgen_thankyouforapplying"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "ugapplgen_applinfolinks"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "ugapplgen_admwebsites"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_directdepositshort"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_aidprioritydateshort"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_aidreminder"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_aidremindershort"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_summeraiddate"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_summeraiddateshort"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_summeraidavail"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_summeraidavailshort"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_acceptrejectawardshort"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_disbursedateashort"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_disbursedatebshort"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_loancounselingshort"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_loanpromissoryshort"))
        self.assertIsNotNone(NOTICE_CATEGORIES.get(
            "studentfinaid_missingdocsshort"))

        categorization = NOTICE_CATEGORIES.get("studentfinaid_aidholdshort")
        self.assertIsNotNone(categorization)
        self.assertEqual(categorization["myuw_category"], "Fees & Finances")
        self.assertFalse(categorization["critical"])
        self.assertEqual(len(categorization["location_tags"]), 1)

        self.assertIsNotNone(NOTICE_CATEGORIES.get("myuwnotice_banner"))
