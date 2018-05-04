from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from myuw.test.api import missing_url, MyuwApiTest
from myuw.views.notice_admin import _get_datetime
from datetime import datetime


class TestNoticeAdmin(MyuwApiTest):

    def test_get_datetime(self):
        string = ""
        self.assertIsNone(_get_datetime(string))

        string = "foobar"
        self.assertIsNone(_get_datetime(string))

        string = "2018-05-08 15:28"
        dt = datetime(2018, 5, 8, 15, 28)
        self.assertEqual(_get_datetime(string), dt)
