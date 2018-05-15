# -*- coding: utf8 -*-
from django.test import TestCase
from datetime import datetime
from myuw.dao.myuw_notice import get_myuw_notices_for_user
from myuw.dao.notice_mapping import categorize_notices
from myuw.test import get_request_with_user, get_request_with_date
from myuw.models.myuw_notice import MyuwNotice


class TestMyuwNotice(TestCase):
    def test_by_date(self):
        notice = MyuwNotice(title="Foo",
                            content="Notice Content",
                            notice_type="Banner",
                            notice_category="Student",
                            start=datetime(2018, 5, 8, 10, 0, 0),
                            end=datetime(2018, 5, 10, 10, 0, 0),
                            is_seattle=True)
        notice.save()
        notice = MyuwNotice(title="Bar",
                            content="Notice Content Two",
                            notice_type="Banner",
                            notice_category="Student",
                            start=datetime(2018, 5, 12, 10, 0, 0),
                            end=datetime(2018, 5, 20, 10, 0, 0),
                            is_seattle=True)
        notice.save()

        request = get_request_with_date("2018-05-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "Foo")

    def test_by_campus(self):
        notice = MyuwNotice(title="Baz",
                            content="Notice Content Three",
                            notice_type="Banner",
                            notice_category="Student",
                            start=datetime(2018, 6, 8, 10, 0, 0),
                            end=datetime(2018, 6, 10, 10, 0, 0),
                            is_seattle=True)
        notice.save()
        notice = MyuwNotice(title="Alert",
                            content="Notice Content Four",
                            notice_type="Banner",
                            notice_category="Student",
                            start=datetime(2018, 6, 8, 10, 0, 0),
                            end=datetime(2018, 6, 20, 10, 0, 0),
                            is_bothell=True)
        notice.save()
        request = get_request_with_date("2018-06-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "Baz")

    def test_no_campus(self):
        notice = MyuwNotice(title="Alert",
                            content="Notice Content Four",
                            notice_type="Banner",
                            notice_category="Student",
                            start=datetime(2018, 6, 8, 10, 0, 0),
                            end=datetime(2018, 6, 20, 10, 0, 0))
        notice.save()
        request = get_request_with_date("2018-06-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "Alert")

    def test_affil(self):
        notice = MyuwNotice(title="Alert",
                            content="Notice Content Four",
                            notice_type="Banner",
                            notice_category="Student",
                            start=datetime(2018, 6, 8, 10, 0, 0),
                            end=datetime(2018, 6, 20, 10, 0, 0),
                            is_instructor=True)
        notice.save()
        notice = MyuwNotice(title="Test",
                            content="Notice Content Five",
                            notice_type="Banner",
                            notice_category="Student",
                            start=datetime(2018, 6, 8, 10, 0, 0),
                            end=datetime(2018, 6, 20, 10, 0, 0),
                            is_student=True)
        notice.save()
        request = get_request_with_date("2018-06-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].title, "Test")

    def test_no_affil(self):
            notice = MyuwNotice(title="Alert",
                                content="Notice Content Four",
                                notice_type="Banner",
                                notice_category="Student",
                                start=datetime(2018, 6, 8, 10, 0, 0),
                                end=datetime(2018, 6, 20, 10, 0, 0))
            notice.save()
            notice = MyuwNotice(title="Test",
                                content="Notice Content Five",
                                notice_type="Banner",
                                notice_category="Student",
                                start=datetime(2018, 6, 8, 10, 0, 0),
                                end=datetime(2018, 6, 20, 10, 0, 0),
                                is_student=True)
            notice.save()
            request = get_request_with_date("2018-06-09")
            get_request_with_user('javerage', request)
            notices = get_myuw_notices_for_user(request)
            self.assertEqual(len(notices), 2)

    def test_myuwnotice_mapping(self):
        notice = MyuwNotice(title="Test",
                            content="Notice Content Five",
                            notice_type="Banner",
                            notice_category="MyUWNotice",
                            start=datetime(2018, 6, 8, 10, 0, 0),
                            end=datetime(2018, 6, 20, 10, 0, 0),
                            is_student=True)
        categorized = categorize_notices([notice])
        self.assertEqual(len(categorized), 1)
        self.assertEqual(categorized[0].location_tags, ['notice_banner'])

    def test_notice_content(self):
        notice = MyuwNotice(title=" ٰ ٱ ٲ ٳ ٴ ٵ ٶ ٷ ٸ ٹ ٺ",
                            content=" ↙ ↚ ↛ ↜ ↝ ↞ ↟ ↠ ↡ ↢ ↣ ↤ ↥ ↦ ↧",
                            notice_type="Banner",
                            notice_category="Student",
                            start=datetime(2018, 6, 8, 10, 0, 0),
                            end=datetime(2018, 6, 20, 10, 0, 0),)
        notice.save()
        self.assertEqual(notice.json_data()['notice_content'],
                         u"<span class=\"notice-title\"> ٰ ٱ ٲ ٳ ٴ ٵ ٶ ٷ ٸ ٹ ٺ"
                         u"</span><span class=\"notice-body-with-title\">"
                         u" ↙ ↚ ↛ ↜ ↝ ↞ ↟ ↠ ↡ ↢ ↣ ↤ ↥ ↦ ↧</span>")
