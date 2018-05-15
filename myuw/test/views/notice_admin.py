from myuw.test.api import missing_url, MyuwApiTest
from django.test.client import RequestFactory
from myuw.views.notice_admin import _get_datetime, _save_notice
from datetime import datetime
from myuw.dao.myuw_notice import get_myuw_notices_for_user
from myuw.test import get_request_with_user, get_request_with_date


class TestNoticeAdmin(MyuwApiTest):

    def test_get_datetime(self):
        string = ""
        self.assertIsNone(_get_datetime(string))

        string = "foobar"
        self.assertIsNone(_get_datetime(string))

        string = "2018-05-08 15:28"
        dt = datetime(2018, 5, 8, 15, 28)
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
            'start_date': "2018-05-25 12:05",
            'end_date': "2018-05-26 12:05",
            'notice_type': 'Foo',
            'notice_category': 'Bar'
        }
        request = rf.post('', notice_context)
        saved = _save_notice(request, {})
        self.assertTrue(saved)

        # end before start
        notice_context = {
            'action': 'save',
            'title': 'The Title',
            'content': "<p>Foobar</p>",
            'start_date': "2018-05-25 12:05",
            'end_date': "2017-05-26 12:05",
            'notice_type': 'Foo',
            'notice_category': 'Bar'
        }
        request = rf.post('', notice_context)
        context = {}
        saved = _save_notice(request, context)
        self.assertFalse(saved)
        self.assertTrue(context['date_error'])

        # no start
        notice_context = {
            'action': 'save',
            'title': 'The Title',
            'content': "<p>Foobar</p>",
            'end_date': "2017-05-26 12:05",
            'notice_type': 'Foo',
            'notice_category': 'Bar'
        }
        request = rf.post('', notice_context)
        context = {}
        saved = _save_notice(request, context)
        self.assertFalse(saved)
        self.assertTrue(context['start_error'])

        # Missing Attrs
        notice_context = {
            'action': 'save',
        }
        request = rf.post('', notice_context)
        context = {}
        saved = _save_notice(request, context)
        self.assertFalse(saved)
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
            'start_date': "2018-05-05 12:05",
            'end_date': "2018-05-26 12:05",
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
