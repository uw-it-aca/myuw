from django.test import TestCase
from myuw.models import BannerMessage
from myuw.dao.messages import get_current_messages, clean_html
from myuw.test import get_request_with_user, get_request_with_date

from datetime import datetime, tzinfo
import pytz


class TestBannerMessageDAO(TestCase):
    def test_get_current(self):
        BannerMessage.objects.all().delete()

        BannerMessage.objects.create(start=datetime(2013, 4, 5),
                                     end=datetime(2013, 4, 7),
                                     message_title='test title',
                                     message_body='test body',
                                     affiliation='student',
                                     is_published=True)

        BannerMessage.objects.create(start=datetime(2011, 4, 5),
                                     end=datetime(2019, 4, 7),
                                     message_title='not current',
                                     message_body='not published',
                                     is_published=False)

        request = get_request_with_date('2013-04-04 00:00:00')
        request = get_request_with_user('javerage', request)
        self.assertEquals(len(get_current_messages(request)), 0)

        request = get_request_with_date('2013-04-05')
        request = get_request_with_user('javerage', request)
        self.assertEquals(len(get_current_messages(request)), 1)

        request = get_request_with_date('2013-04-07')
        request = get_request_with_user('javerage', request)
        self.assertEquals(len(get_current_messages(request)), 1)

        request = get_request_with_date('2013-04-08')
        request = get_request_with_user('javerage', request)
        self.assertEquals(len(get_current_messages(request)), 0)

        request = get_request_with_date('2013-04-07')
        request = get_request_with_user('bill', request)
        self.assertEquals(len(get_current_messages(request)), 0)

    def test_group_filter(self):
        BannerMessage.objects.all().delete()

        BannerMessage.objects.create(start=datetime(2013, 4, 5),
                                     end=datetime(2013, 4, 7),
                                     message_title='test title',
                                     message_body='test body',
                                     group_id='uw_test_group',
                                     is_published=True)

        request = get_request_with_date('2013-04-07')
        request = get_request_with_user('javerage', request)

        by_settings = 'authz_group.authz_implementation.settings.Settings'
        with self.settings(AUTHZ_GROUP_BACKEND=by_settings,
                           AUTHZ_GROUP_MEMBERS={"uw_test_group": []}):
                self.assertEquals(len(get_current_messages(request)), 0)

        with_javerage = {"uw_test_group": ["javerage"]}
        with self.settings(AUTHZ_GROUP_BACKEND=by_settings,
                           AUTHZ_GROUP_MEMBERS=with_javerage):
                self.assertEquals(len(get_current_messages(request)), 1)

    def test_html_cleanup(self):
        out = clean_html('<a href="http://uw.edu">UW</a>')
        self.assertEquals(out, '<a href="http://uw.edu">UW</a>')

        out = clean_html("<h2>h2</h2>")
        self.assertEquals(out, "<h2>h2</h2>")

        out = clean_html("<b><i>x")
        self.assertEquals(out, "<b><i>x</i></b>")

        out = clean_html("<script>alert('x');</script>")
        self.assertEquals(out, "&lt;script&gt;alert('x');&lt;/script&gt;")
