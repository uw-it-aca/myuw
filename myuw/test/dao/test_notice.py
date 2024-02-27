# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from myuw.dao.notice import _get_notices_by_regid
from myuw.test import (
    get_request_with_date, get_request,
    fdao_sws_override, fdao_pws_override)


@fdao_sws_override
@fdao_pws_override
class TestNotices(TestCase):
    def setUp(self):
        get_request()

    def test_get_notice_by_regid(self):
        # no regid
        notices = _get_notices_by_regid(None)
        self.assertEqual(notices, None)

        # bad regid
        notices = _get_notices_by_regid("99999678901234567890123456789012")
        self.assertEqual(len(notices), 0)

        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = _get_notices_by_regid(regid)
        self.assertIsNotNone(notices)
        self.assertEqual(len(notices), 24)

        self.assertEqual(notices[0].custom_category, "Holds")
        self.assertEqual(
            notices[0].location_tags,
            ['notices_holds', 'reg_card_holds'])
        self.assertTrue(notices[0].is_critical)

        self.assertEqual(
            notices[13].custom_category, "Fees & Finances")
        self.assertEqual(
            notices[13].location_tags,
            ['tuition_aid_reminder_title'])
        self.assertFalse(notices[12].is_critical)

        regid = "9136CCB8F66711D5BE060004AC494F31"
        notices = _get_notices_by_regid(regid)
        self.assertIsNotNone(notices)
        self.assertEqual(len(notices), 35)
        self.assertEqual(notices[12].custom_category,
                         "Fees & Finances")
        self.assertFalse(notices[12].is_critical)

        regid = "12345678901234567890123456789012"
        notices = _get_notices_by_regid(regid)
        self.assertIsNotNone(notices)
        self.assertEqual(len(notices), 31)
        for notice in notices:
            if notice.notice_type == "DirectDeposit":
                self.assertEqual(notice.location_tags,
                                 ['tuition_direct_deposit'])
                self.assertTrue(notice.is_critical)

            if notice.notice_type == "DirectDepositShort":
                self.assertEqual(notice.location_tags,
                                 ['tuition_direct_deposit_title'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "AidPriorityDate":
                self.assertEqual(
                    notice.location_tags,
                    ['tuition_aid_prioritydate', 'notices_date_sort'])
                self.assertTrue(notice.is_critical)

            if notice.notice_type == "AidPriorityDateShort":
                self.assertEqual(notice.location_tags,
                                 ['tuition_aid_prioritydate_title'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "AidReminder":
                self.assertEqual(notice.location_tags,
                                 ['tuition_aid_reminder'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "AidReminderShort":
                self.assertEqual(notice.location_tags,
                                 ['tuition_aid_reminder_title'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "SummerAidDate":
                self.assertEqual(
                    notice.location_tags,
                    ['tuition_summeraid_date', 'notices_date_sort'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "SummerAidDateShort":
                self.assertEqual(notice.location_tags,
                                 ['tuition_summeraid_date_title'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "SummerAidAvail":
                self.assertEqual(
                    notice.location_tags,
                    ['tuition_summeraid_avail', 'reg_summeraid_avail'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "SummerAidAvailShort":
                self.assertEqual(
                    notice.location_tags,
                    ['tuition_summeraid_avail_title',
                     'reg_summeraid_avail_title'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "AcceptRejectAward":
                self.assertEqual(
                    notice.location_tags, ['tuition_acceptreject'])
                self.assertTrue(notice.is_critical)

            if notice.notice_type == "AcceptRejectAwardShort":
                self.assertEqual(
                    notice.location_tags, ['tuition_acceptreject_title'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "DisburseDateA":
                self.assertEqual(
                    notice.location_tags,
                    ['tuition_disbursedateA', 'notices_date_sort'])
                self.assertTrue(notice.is_critical)

            if notice.notice_type == "DisburseDateAShort":
                self.assertEqual(
                    notice.location_tags,
                    ['tuition_disbursedateA_title'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "DisburseDateB":
                self.assertEqual(
                    notice.location_tags,
                    ['tuition_disbursedateB', 'notices_date_sort'])
                self.assertTrue(notice.is_critical)

            if notice.notice_type == "DisburseDateBShort":
                self.assertEqual(
                    notice.location_tags,
                    ['tuition_disbursedateB_title'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "LoanCounseling":
                self.assertEqual(
                    notice.location_tags, ['tuition_loancounseling'])
                self.assertTrue(notice.is_critical)

            if notice.notice_type == "LoanCounselingShort":
                self.assertEqual(
                    notice.location_tags,
                    ['tuition_loancounseling_title'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "LoanPromissory":
                self.assertEqual(
                    notice.location_tags, ['tuition_loanpromissory'])
                self.assertTrue(notice.is_critical)

            if notice.notice_type == "LoanPromissoryShort":
                self.assertEqual(
                    notice.location_tags,
                    ['tuition_loanpromissory_title'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "MissingDocs":
                self.assertEqual(
                    notice.location_tags, ['tuition_missingdocs'])
                self.assertTrue(notice.is_critical)

            if notice.notice_type == "MissingDocsShort":
                self.assertEqual(
                    notice.location_tags, ['tuition_missingdocs_title'])
                self.assertFalse(notice.is_critical)

            if notice.notice_type == "AidHold":
                self.assertEqual(
                    notice.location_tags, ['tuition_aidhold'])
                self.assertTrue(notice.is_critical)

            if notice.notice_type == "AidHoldShort":
                self.assertEqual(
                    notice.location_tags, ['tuition_aidhold_title'])
                self.assertFalse(notice.is_critical)

        # test MUWM-4535
        regid = "FE36CCB8F66711D5BE060004AC494F31"  # jnew
        notices = _get_notices_by_regid(regid)
        self.assertEqual(len(notices), 23)
        self.assertEqual(notices[16].notice_type, 'HSImmunBlock')
        self.assertEqual(notices[17].notice_type, 'AdvOrientRegDateB')
        self.assertEqual(notices[18].notice_type, 'HSImmunReqDateA')
        self.assertEqual(notices[19].notice_type, 'HSImmunReqDateB')

        regid = "FE36CCB8F66711D5BE060004AC494FCD"  # jbothell
        notices = _get_notices_by_regid(regid)
        for notice in notices:
            if notice.notice_type == "Fees & Finances":
                self.assertTrue("tuition_due_date" in notice.location_tags)
                self.assertTrue(notice.is_critical)
