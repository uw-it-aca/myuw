from django.test import TestCase
from myuw.dao.notice import _get_notices_by_regid
from myuw.test import FDAO_SWS, FDAO_PWS, get_request_with_date,\
    get_request_with_user


class TestNotices(TestCase):
    def setUp(self):
        get_request_with_user('javerage')

    def test_get_notice_by_regid(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):

            # no regid
            notices = _get_notices_by_regid(None)
            self.assertEquals(notices, None)

            # bad regid
            notices = _get_notices_by_regid("99999678901234567890123456789012")
            self.assertEquals(len(notices), 0)

            regid = "9136CCB8F66711D5BE060004AC494FFE"
            notices = _get_notices_by_regid(regid)
            self.assertIsNotNone(notices)
            self.assertEquals(len(notices), 23)

            self.assertEquals(notices[0].custom_category, "Holds")
            self.assertEquals(notices[0].location_tags, ['notices_holds',
                                                         'reg_card_holds'])
            self.assertTrue(notices[0].is_critical)

            self.assertEquals(notices[12].custom_category,
                              "Fees & Finances")
            self.assertEquals(notices[12].location_tags,
                              ['tuition_aid_reminder_title'])
            self.assertFalse(notices[12].is_critical)

            regid = "9136CCB8F66711D5BE060004AC494F31"
            notices = _get_notices_by_regid(regid)
            self.assertIsNotNone(notices)
            self.assertEquals(len(notices), 31)
            self.assertEquals(notices[12].custom_category,
                              "Fees & Finances")
            self.assertFalse(notices[12].is_critical)

            regid = "12345678901234567890123456789012"
            notices = _get_notices_by_regid(regid)
            self.assertIsNotNone(notices)
            self.assertEquals(len(notices), 31)
            for notice in notices:
                if notice.notice_type == "DirectDeposit":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_direct_deposit'])
                    self.assertTrue(notice.is_critical)

                if notice.notice_type == "DirectDepositShort":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_direct_deposit_title'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "AidPriorityDate":
                    self.assertEquals(
                        notice.location_tags,
                        ['tuition_aid_prioritydate', 'notices_date_sort'])
                    self.assertTrue(notice.is_critical)

                if notice.notice_type == "AidPriorityDateShort":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_aid_prioritydate_title'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "AidReminder":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_aid_reminder'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "AidReminderShort":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_aid_reminder_title'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "SummerAidDate":
                    self.assertEquals(
                        notice.location_tags,
                        ['tuition_summeraid_date', 'notices_date_sort'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "SummerAidDateShort":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_summeraid_date_title'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "SummerAidAvail":
                    self.assertEquals(
                        notice.location_tags,
                        ['tuition_summeraid_avail', 'reg_summeraid_avail'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "SummerAidAvailShort":
                    self.assertEquals(
                        notice.location_tags,
                        ['tuition_summeraid_avail_title',
                         'reg_summeraid_avail_title'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "AcceptRejectAward":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_acceptreject'])
                    self.assertTrue(notice.is_critical)

                if notice.notice_type == "AcceptRejectAwardShort":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_acceptreject_title'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "DisburseDateA":
                    self.assertEquals(
                        notice.location_tags,
                        ['tuition_disbursedateA', 'notices_date_sort'])
                    self.assertTrue(notice.is_critical)

                if notice.notice_type == "DisburseDateAShort":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_disbursedateA_title'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "DisburseDateB":
                    self.assertEquals(
                        notice.location_tags,
                        ['tuition_disbursedateB', 'notices_date_sort'])
                    self.assertTrue(notice.is_critical)

                if notice.notice_type == "DisburseDateBShort":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_disbursedateB_title'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "LoanCounseling":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_loancounseling'])
                    self.assertTrue(notice.is_critical)

                if notice.notice_type == "LoanCounselingShort":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_loancounseling_title'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "LoanPromissory":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_loanpromissory'])
                    self.assertTrue(notice.is_critical)

                if notice.notice_type == "LoanPromissoryShort":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_loanpromissory_title'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "MissingDocs":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_missingdocs'])
                    self.assertTrue(notice.is_critical)

                if notice.notice_type == "MissingDocsShort":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_missingdocs_title'])
                    self.assertFalse(notice.is_critical)

                if notice.notice_type == "AidHold":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_aidhold'])
                    self.assertTrue(notice.is_critical)

                if notice.notice_type == "AidHoldShort":
                    self.assertEquals(notice.location_tags,
                                      ['tuition_aidhold_title'])
                    self.assertFalse(notice.is_critical)
