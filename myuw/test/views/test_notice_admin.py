# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest.mock import patch
from myuw.test.api import MyuwApiTest
from django.test.client import RequestFactory
from myuw.models.myuw_notice import MyuwNotice
from myuw.views.notice_admin import _get_datetime, _get_html, _save_notice
from myuw.dao.myuw_notice import get_myuw_notices_for_user
from myuw.test import get_request_with_user, get_request_with_date

CONTENT = (
    "<p>Your Husky card is your key to efficiency on " +
    "campus and serves as your University ID, providing access " +
    "to eligible services such as dining plans, facilities, " +
    "transportation, UW libraries, and so much more.</p>\n<p><a " +
    "href=\"http://hfs.uw.edu/Husky-Card-Services/submit-a-photo" +
    "\">Submit your photo online</a>\nto be able to have your " +
    "Husky card printed and sent to you by mail. Students with " +
    "an international address should submit a photo online and " +
    "plan to pick up their Husky card on campus. Visit the <a " +
    "href=\"https://hfs.uw.edu/Husky-Card-Services/Operations-" +
    "Updates\" title=\"https://hfs.uw.edu/Husky-Card-Services/" +
    "Operations-Updates\">Husky Card Operations</a> page for " +
    "more information.\n</p>")


class TestNoticeAdmin(MyuwApiTest):

    def _get_request(self, notice):
        return RequestFactory().post('', notice)

    def test_get_datetime(self):
        self.assertIsNone(_get_datetime(""))
        self.assertIsNone(_get_datetime(None))
        string = "2018-05-08 15:28"
        self.assertEqual(str(_get_datetime(string)),
                         "2018-05-08 15:28:00-07:00")
        string = "2018-05-08T15:28"
        self.assertEqual(str(_get_datetime(string)),
                         "2018-05-08 15:28:00-07:00")
        string = "2018-05-08T15:28:00-07:00"
        self.assertEqual(str(_get_datetime(string)),
                         "2018-05-08 15:28:00-07:00")

    def test_get_html(self):
        self.assertIsNone(_get_html(None))
        self.assertEqual(_get_html(''), "")
        self.assertIsNotNone(_get_html(CONTENT))

    @patch.object(MyuwNotice, 'save')
    def test_sql_error_save(self, mock):
        request = self._get_request(
            {
                'action': 'save',
                "title": "Test",
                "start_date": "2022-04-12 11:25",
                "end_date": "2022-04-15 11:25",
                "content": CONTENT,
                "notice_type": "Banner",
                "notice_category": "MyUWNotice",
                "is_critical": False,
                'affil': ['is_employee'],
                'target_group': ''
            })
        context = {}
        mock.side_effect = Exception('Error!')
        self.assertFalse(_save_notice(request, context))
        self.assertTrue(context['sql_error'])

    def test_save_new_notice(self):
        request = self._get_request({})
        saved = _save_notice(request, {})
        self.assertFalse(saved)

        request = self._get_request(
            {
                'action': 'save',
                'title': 'The Title ',
                'content': "<p>Foobar</p>",
                'affil': 'is_intl_stud',
                'campus': 'is_seattle',
                'start_date': '2018-05-25 12:00',
                'end_date': '2018-05-26 12:00',
                'notice_type': 'Foo',
                'notice_category': 'Bar',
                'target_group': ' uw_group '
            })
        self.assertTrue(_save_notice(request, {}))

        entries = MyuwNotice.objects.all()
        self.assertEqual(len(entries), 1)
        self.assertIsNotNone(entries[0].json_data())
        self.assertIsNotNone(str(entries[0]))
        self.assertIsNotNone(entries[0].get_notice_content())
        self.assertTrue(entries[0].is_intl_stud)
        self.assertTrue(entries[0].is_seattle)
        self.assertTrue(entries[0].has_target_group())
        self.assertEqual(entries[0].title, "The Title")
        self.assertEqual(entries[0].target_group, "uw_group")

        # end before start
        request = self._get_request(
            {
                'action': 'save',
                'title': 'The Title',
                'content': "<p>Foobar</p>",
                'start_date': "2018-05-25 12:05",
                'end_date': "2017-05-26 12:05",
                'notice_type': 'Foo',
                'notice_category': 'Bar'
            })
        context = {}
        self.assertFalse(_save_notice(request, context))
        self.assertTrue(context['date_error'])

        # no start
        request = self._get_request(
            {
                'action': 'save',
                'title': 'The Title',
                'content': "<p>Foobar</p>",
                'end_date': "2017-05-26 12:05",
                'notice_type': 'Foo',
                'notice_category': 'Bar'
            })
        context = {}
        self.assertFalse(_save_notice(request, context))
        self.assertTrue(context['start_error'])

        # Missing Attrs
        request = self._get_request({'action': 'save', })
        context = {}
        self.assertFalse(_save_notice(request, context))
        print(context)
        self.assertTrue(context['start_error'])
        self.assertTrue(context['type_error'])
        self.assertTrue(context['category_error'])
        self.assertTrue(context['title_error'])
        self.assertTrue(context['content_error'])

    def test_content_allowed_tags(self):
        request = self._get_request(
            {
                'action': 'save',
                'title': '<b>The</b> Title',
                'content': "<p>allowed tag</p> <span>not allowed</span>",
                'start_date': "2018-05-05 12:05",
                'end_date': "2018-05-26 12:05",
                'notice_type': 'Foo',
                'notice_category': 'Bar'
            })
        _save_notice(request, {})

        request = get_request_with_date("2018-05-09")
        get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)

        self.assertEqual(notices[0].title, "<b>The</b> Title")

        self.assertEqual(
            notices[0].content,
            "<p>allowed tag</p> <span>not allowed</span>")

    def test_target_group(self):
        notice_context = {
            'action': 'save',
            'title': 'Test Edit',
            'content': "Foo",
            'start_date': "2013-03-27 13:00",
            'end_date': "2013-05-06 23:13",
            'notice_type': 'Foo',
            'notice_category': 'Bar',
            'target_group': 'u_astratst_myuw_test-support-admin'
        }
        request = self._get_request(notice_context)
        self.assertTrue(_save_notice(request, {}))

        notice_context['action'] = 'edit'
        notice_context['content'] = "Bar"
        notice_context['title'] = 'Edited'

        entries = MyuwNotice.objects.all()
        self.assertEqual(len(entries), 1)

        request = self._get_request(notice_context)
        self.assertTrue(_save_notice(request, {},
                                     notice_id=entries[0].id))

        request = get_request_with_date("2013-04-09")
        request = get_request_with_user('javerage', request)
        notices = get_myuw_notices_for_user(request)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0].content, 'Bar')
        self.assertEqual(notices[0].target_group,
                         'u_astratst_myuw_test-support-admin')
