import pytz
from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from uw_sws.notice import get_notices_by_regid
from myuw.dao.notice_mapping import map_notice_category,\
    get_open_date, get_close_date, is_after_eof_days_after_open,\
    is_before_bof_days_before_close, apply_showhide, categorize_notices
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request


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
        self.assertEquals(len(notices), 23)
        notice = notices[10]
        self.assertEquals(notice.custom_category, "Fees & Finances")
        self.assertEquals(notice.location_tags,
                          ['tuition_aid_prioritydate_title'])
        self.assertFalse(notice.is_critical)

    def test_get_open_date(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = categorize_notices(get_notices_by_regid(regid))
        notice = notices[9]
        self.assertTrue(notice.is_critical)
        open_date = get_open_date(notice)
        open = timezone.get_current_timezone().localize(
            datetime(2013, 1, 1, 0, 0, 0)).astimezone(pytz.utc)
        self.assertEquals(open_date, open)

    def test_get_close_date(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = categorize_notices(get_notices_by_regid(regid))
        notice = notices[9]
        close_date = get_close_date(notice)
        close = timezone.get_current_timezone().localize(
            datetime(2013, 2, 28, 0, 0, 0)).astimezone(pytz.utc)
        self.assertEquals(close_date, close)

    def test_is_after_eof_days_after_open(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = categorize_notices(get_notices_by_regid(regid))
        notice = notices[9]
        now = timezone.get_current_timezone().localize(
            datetime(2013, 1, 15, 0, 0, 0)).astimezone(pytz.utc)
        self.assertFalse(is_after_eof_days_after_open(now, notice, 14))

        now = timezone.get_current_timezone().localize(
            datetime(2013, 1, 16, 0, 0, 0)).astimezone(pytz.utc)
        self.assertTrue(is_after_eof_days_after_open(now, notice, 14))

    def test_is_before_bof_days_before_close(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = categorize_notices(get_notices_by_regid(regid))
        notice = notices[9]
        now = timezone.get_current_timezone().localize(
            datetime(2013, 2, 14, 0, 0, 0)).astimezone(pytz.utc)
        self.assertFalse(is_before_bof_days_before_close(now, notice, 14))
        now = timezone.get_current_timezone().localize(
            datetime(2013, 2, 13, 0, 0, 0)).astimezone(pytz.utc)
        self.assertTrue(is_before_bof_days_before_close(now, notice, 14))

    def test_apply_showhide(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"

        # within 14 days after open
        now_request = get_request_with_date("2013-01-15")
        notices = apply_showhide(
            now_request,
            categorize_notices(get_notices_by_regid(regid)))
        notice = notices[9]
        self.assertTrue(notice.is_critical)

        # after 14 days after open
        now_request = get_request_with_date("2013-01-16")
        notices = apply_showhide(
            now_request,
            categorize_notices(get_notices_by_regid(regid)))
        notice = notices[9]
        self.assertFalse(notice.is_critical)

        # before 14 days before close
        now_request = get_request_with_date("2013-02-12")
        notices = apply_showhide(
            now_request,
            categorize_notices(get_notices_by_regid(regid)))
        notice = notices[9]
        self.assertFalse(notice.is_critical)

        # within 14 days before close
        now_request = get_request_with_date("2013-02-13")
        notices = apply_showhide(
            now_request,
            categorize_notices(get_notices_by_regid(regid)))
        notice = notices[9]
        self.assertTrue(notice.is_critical)
