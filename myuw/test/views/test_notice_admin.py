# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.api import missing_url, MyuwApiTest
from django.test.client import RequestFactory
from myuw.models.myuw_notice import MyuwNotice
from myuw.views.notice_admin import _get_datetime, _save_notice
from datetime import datetime
from myuw.dao.myuw_notice import get_myuw_notices_for_user
from myuw.test import get_request_with_user, get_request_with_date
from myuw.test.dao.test_myuw_notice import get_datetime_with_tz


class TestNoticeAdmin(MyuwApiTest):

    def test_get_datetime(self):
        string = ""
        self.assertIsNone(_get_datetime(string))

        string = "foobar"
        self.assertIsNone(_get_datetime(string))

        string = "2018-05-08 15:28"
        self.assertEqual(str(_get_datetime(string)),
                         "2018-05-08 15:28:00-07:00")

        string = "2013-03-28 10:00:00+00:00"
        dt = get_datetime_with_tz(2013, 3, 28, 3)
        self.assertEqual(_get_datetime(string), dt)

    def test_save_new_notice(self):
        rf = RequestFactory()
        request = rf.post('', {})

        saved = _save_notice(request, {})
        self.assertFalse(saved)

        notice_context = {
            'action': 'save',
            'title': 'The Title',
            'content': "<p>Foobar</p>",
            'affil': 'is_intl_stud',
            'campus': 'is_seattle',
            'start_date': '2018-05-25 12:00',
            'end_date': '2018-05-26 12:00',
            'notice_type': 'Foo',
            'notice_category': 'Bar',
            'target_group': 'uw_group'
        }
        request = rf.post('', notice_context)
        self.assertTrue(_save_notice(request, {}))

        entries = MyuwNotice.objects.all()
        self.assertEqual(len(entries), 1)
        self.assertIsNotNone(entries[0].json_data())
        self.assertIsNotNone(str(entries[0]))
        self.assertIsNotNone(entries[0].get_notice_content())
        self.assertTrue(entries[0].is_intl_stud)
        self.assertTrue(entries[0].is_seattle)
        self.assertTrue(entries[0].has_target_group())

        # end before start
        notice_context = {
            'action': 'save',
            'title': 'The Title',
            'content': "<p>Foobar</p>",
            'start_date': "2018-05-25T12:05:00+00:00",
            'end_date': "2017-05-26T12:05:00+00:00",
            'notice_type': 'Foo',
            'notice_category': 'Bar'
        }
        request = rf.post('', notice_context)
        context = {}
        self.assertFalse(_save_notice(request, context))
        self.assertTrue(context['date_error'])

        # no start
        notice_context = {
            'action': 'save',
            'title': 'The Title',
            'content': "<p>Foobar</p>",
            'end_date': "2017-05-26T12:05:00+00:00",
            'notice_type': 'Foo',
            'notice_category': 'Bar'
        }
        request = rf.post('', notice_context)
        context = {}
        self.assertFalse(_save_notice(request, context))
        self.assertTrue(context['start_error'])

        # Missing Attrs
        notice_context = {
            'action': 'save',
        }
        request = rf.post('', notice_context)
        context = {}
        self.assertFalse(_save_notice(request, context))
        self.assertTrue(context['start_error'])
        self.assertTrue(context['type_error'])
        self.assertTrue(context['category_error'])
        self.assertTrue(context['title_error'])
        self.assertTrue(context['content_error'])

    def test_html_content(self):
        notice_context = {
            'action': 'save',
            'title': '<b>The</b> <p>Title</p>',
            'content': "<p>allowed tag</p> <script>not allowed</script>",
            'start_date': "2018-05-05T12:05:00+00:00",
            'end_date': "2018-05-26T12:05:00+00:00",
            'notice_type': 'Foo',
            'notice_category': 'Bar'
        }
        rf = RequestFactory()
        request = rf.post('', notice_context)
        _save_notice(request, {})

        request = get_request_with_date("2018-05-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)

        self.assertEqual(notices[0].title, "<b>The</b> &lt;p&gt;"
                                           "Title&lt;/p&gt;")

        self.assertEqual(notices[0].content, "<p>allowed tag</p> &lt;script"
                                             "&gt;not allowed&lt;/script&gt;")

    def test_edit_notice(self):
        notice_context = {
            'action': 'save',
            'title': 'Test Edit',
            'content': "Foo",
            'start_date': "2013-03-27T13:00:00+00:00",
            'end_date': "2013-05-06T23:13:00+00:00",
            'notice_type': 'Foo',
            'notice_category': 'Bar',
            'target_group': 'u_astratst_myuw_test-support-admin'
        }
        rf = RequestFactory()
        request = rf.post('', notice_context)
        self.assertTrue(_save_notice(request, {}))

        notice_context['action'] = 'edit'
        notice_context['content'] = "Bar"
        notice_context['title'] = 'Edited'

        entries = MyuwNotice.objects.all()
        self.assertEqual(len(entries), 1)

        request = rf.post('', notice_context)
        self.assertTrue(_save_notice(request, {},
                                     notice_id=entries[0].id))

        request = get_request_with_date("2013-04-09")
        request = get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].content, 'Bar')
        self.assertEqual(notices[0].target_group,
                         'u_astratst_myuw_test-support-admin')
