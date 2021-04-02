# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TransactionTestCase
from myuw.models import BannerMessage
from myuw.dao.messages import get_current_messages, clean_html
from myuw.test import get_request_with_user, get_request_with_date
from myuw.test.dao.test_myuw_notice import get_datetime_with_tz


class TestBannerMessageDAO(TransactionTestCase):
    def test_get_current(self):
        BannerMessage.objects.create(start=get_datetime_with_tz(2013, 4, 5, 0),
                                     end=get_datetime_with_tz(2013, 4, 7, 0),
                                     message_title='test title',
                                     message_body='test body',
                                     affiliation='student',
                                     is_published=True)

        b2 = BannerMessage.objects.create(
            start=get_datetime_with_tz(2011, 4, 5, 0),
            end=get_datetime_with_tz(2019, 4, 7, 0),
            message_title='not current',
            message_body='not published',
            is_published=False)

        request = get_request_with_date('2013-04-04 00:00:00')
        request = get_request_with_user('javerage', request)
        self.assertEquals(len(get_current_messages(request)), 0)

        request = get_request_with_date('2013-04-05')
        request = get_request_with_user('javerage', request)
        self.assertEquals(len(get_current_messages(request)), 1)

        request = get_request_with_date('2013-04-06')
        request = get_request_with_user('javerage', request)
        self.assertEquals(len(get_current_messages(request)), 1)

        request = get_request_with_date('2013-04-07')
        request = get_request_with_user('javerage', request)
        self.assertEquals(len(get_current_messages(request)), 0)

        request = get_request_with_date('2013-04-07')
        request = get_request_with_user('bill', request)
        self.assertEquals(len(get_current_messages(request)), 0)

        request.GET = {"banner": b2.preview_id}
        self.assertEquals(len(get_current_messages(request)), 1)

        request.GET = {"banner": None}
        self.assertEquals(len(get_current_messages(request)), 0)

        request.GET = {"banner": "AAbb"}
        self.assertEquals(len(get_current_messages(request)), 0)

    def test_group_filter(self):
        BannerMessage.objects.create(
            start=get_datetime_with_tz(2013, 4, 5, 0),
            end=get_datetime_with_tz(2013, 4, 7, 0),
            message_title='test title',
            message_body='test body',
            group_id='uw_test_group',
            is_published=True)

        request = get_request_with_date('2013-04-06')
        request = get_request_with_user('javerage', request)
        self.assertEquals(len(get_current_messages(request)), 1)

    def test_html_cleanup(self):
        out = clean_html('Awesome: <i class="fa fa-bullhorn"></i>')
        self.assertEquals(out, 'Awesome: <i class="fa fa-bullhorn"></i>')

        out = clean_html('<span style="font-size: 12px; background-image: x;' +
                         'color: red;">OK</span>')

        self.assertEquals(out, '<span style="font-size: 12px; color: red;">' +
                               'OK</span>')

        out = clean_html('<i aria-hidden="true"></i>')
        self.assertEquals(out, '<i aria-hidden="true"></i>')

        out = clean_html('<a href="http://uw.edu">UW</a>')
        self.assertEquals(out, '<a href="http://uw.edu">UW</a>')

        out = clean_html("<h2>h2</h2>")
        self.assertEquals(out, "<h2>h2</h2>")

        out = clean_html("<b><i>x")
        self.assertEquals(out, "<b><i>x</i></b>")

        out = clean_html("<script>alert('x');</script>")
        self.assertEquals(out, "&lt;script&gt;alert('x');&lt;/script&gt;")
