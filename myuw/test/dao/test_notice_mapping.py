# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, override_settings
from datetime import datetime, timezone
from django.utils.timezone import get_default_timezone
from django.conf import settings
from uw_sws.notice import get_notices_by_regid
from myuw.dao.notice_mapping import (
    map_notice_category, apply_showhide, categorize_notices,
    get_open_date, get_close_date, is_after_eof_days_after_open,
    is_before_bof_days_before_close)
from myuw.models.myuw_notice import MyuwNotice
from myuw.test import (
    fdao_sws_override, fdao_pws_override,
    get_request_with_date, get_request)


@fdao_sws_override
@fdao_pws_override
class TestMapNotices(TestCase):
    def setUp(self):
        get_request()

    def test_map_notice_category(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"

        notices = get_notices_by_regid(regid)
        self.assertEquals(len(notices), 28)

        notice = map_notice_category(notices[0])
        self.assertEquals(notice.custom_category, "Holds")
        self.assertEquals(notice.location_tags, ['notices_holds',
                                                 'reg_card_holds'])
        self.assertTrue(notice.is_critical)

        notice = map_notice_category(notices[4])
        self.assertEquals(notice.custom_category, "Registration")
        self.assertEquals(notice.location_tags, ['reg_card_messages'])
        self.assertTrue(notice.is_critical)

        notice = map_notice_category(notices[9])
        self.assertEquals(notice.custom_category, "Admission")
        self.assertEquals(notice.location_tags, ['checklist_feespaid'])
        self.assertFalse(notice.is_critical)

        notice = map_notice_category(notices[11])
        self.assertEquals(notice.custom_category, "Fees & Finances")
        self.assertEquals(notice.location_tags, ['tuition_direct_deposit'])
        self.assertTrue(notice.is_critical)

        notice = map_notice_category(notices[14])
        self.assertEquals(notice.custom_category, "Fees & Finances")
        self.assertEquals(notice.location_tags,
                          ['tuition_aid_prioritydate_title'])
        self.assertFalse(notice.is_critical)

        notice = map_notice_category(notices[20])
        self.assertEquals(notice.location_tags,
                          ['tuition_summeraid_avail_title',
                           'reg_summeraid_avail_title'])
        self.assertFalse(notice.is_critical)

    def test_categorize_notices(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = categorize_notices(get_notices_by_regid(regid))
        notice = notices[10]
        self.assertEquals(notice.custom_category, "Fees & Finances")
        self.assertEquals(notice.location_tags,
                          ["tuition_aid_prioritydate", "notices_date_sort"])
        self.assertTrue(notice.is_critical)

    def test_get_date(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = categorize_notices(get_notices_by_regid(regid))
        notice = notices[10]
        open_date = get_open_date(notice)
        self.assertEquals(str(open_date), "2013-01-01 08:00:00+00:00")
        close_date = get_close_date(notice)
        self.assertEquals(str(close_date), "2013-02-28 08:00:00+00:00")

    @override_settings(TIME_ZONE='America/Los_Angeles')
    def test_is_after_eof_days_after_open(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = categorize_notices(get_notices_by_regid(regid))
        notice = notices[10]
        tz = get_default_timezone()
        d1 = datetime(2013, 1, 15, 0, 0, 0, tzinfo=tz).astimezone(timezone.utc)
        self.assertFalse(is_after_eof_days_after_open(d1, notice, 14))

        d2 = datetime(2013, 1, 16, 0, 0, 0, tzinfo=tz).astimezone(timezone.utc)
        self.assertTrue(is_after_eof_days_after_open(d2, notice, 14))

    @override_settings(TIME_ZONE='America/Los_Angeles')
    def test_is_before_bof_days_before_close(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = categorize_notices(get_notices_by_regid(regid))
        notice = notices[10]
        tz = get_default_timezone()
        d1 = datetime(2013, 2, 14, 0, 0, 0, tzinfo=tz).astimezone(timezone.utc)
        self.assertFalse(is_before_bof_days_before_close(d1, notice, 14))

        d2 = datetime(2013, 2, 13, 0, 0, 0, tzinfo=tz).astimezone(timezone.utc)
        self.assertTrue(is_before_bof_days_before_close(d2, notice, 14))

    def test_apply_showhide(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"

        # within 14 days after open
        now_request = get_request_with_date("2013-01-15")
        notices = apply_showhide(
            now_request,
            categorize_notices(get_notices_by_regid(regid)))
        notice = notices[10]
        self.assertTrue(notice.is_critical)

        # after 14 days after open
        now_request = get_request_with_date("2013-01-16")
        notices = apply_showhide(
            now_request,
            categorize_notices(get_notices_by_regid(regid)))
        notice = notices[10]
        self.assertFalse(notice.is_critical)

        # before 14 days before close
        now_request = get_request_with_date("2013-02-12")
        notices = apply_showhide(
            now_request,
            categorize_notices(get_notices_by_regid(regid)))
        notice = notices[10]
        self.assertFalse(notice.is_critical)

        # within 14 days before close
        now_request = get_request_with_date("2013-02-13")
        notices = apply_showhide(
            now_request,
            categorize_notices(get_notices_by_regid(regid)))
        notice = notices[10]
        self.assertTrue(notice.is_critical)

        # test MUWM-4535
        regid = "FE36CCB8F66711D5BE060004AC494F31"
        notices = get_notices_by_regid(regid)
        self.assertEquals(len(notices), 25)
        notice = map_notice_category(notices[18])
        self.assertEquals(notice.custom_category, 'Registration')
        self.assertEquals(notice.location_tags,
                          ['notices_date_sort'])

        notice = map_notice_category(notices[19])
        self.assertEquals(notice.custom_category, 'Admission')
        self.assertEquals(notice.location_tags,
                          ['checklist_no_orient'])

        notice = map_notice_category(notices[20])
        self.assertEquals(notice.custom_category, 'Registration')
        self.assertEquals(notice.location_tags,
                          ['notices_date_sort'])

        notice = map_notice_category(notices[21])
        self.assertEquals(notice.custom_category, 'Registration')
        self.assertEquals(notice.location_tags,
                          ['notices_date_sort'])

        # test MUWM-4676
        notice21 = MyuwNotice(title="Test",
                              content="...",
                              notice_type="Banner",
                              notice_category="MyUWNotice",
                              is_critical=True,
                              start="2020-04-02T07:01:00+00:00",
                              end="2020-04-10T00:58:00+00:00",
                              target_group="")
        notice = map_notice_category(notice21)
        self.assertEquals(notice.custom_category, 'MyUW Banner Notice')
        self.assertTrue(notice.is_critical)
