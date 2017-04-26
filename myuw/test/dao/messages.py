import datetime
from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.library import _get_account_by_uwnetid
from myuw.dao.library import get_subject_guide_by_section
from myuw.dao.schedule import _get_schedule
from uw_sws.models import Term
from myuw.test import fdao_pws_override, fdao_sws_override, get_request
from myuw.dao.messages import get_filtered_messages


@fdao_pws_override
@fdao_sws_override
class TestMessages(TestCase):

    def setUp(self):
        get_request()

    def test_get_filtered_messages(self):
        with self.settings(SERU_LIST=None):
            current_date = datetime.date(2013, 4, 12)
            messages = get_filtered_messages(current_date, "javerage")
            self.assertEquals(len(messages), 1)

            messages = get_filtered_messages(current_date, "jnotosoaverage")
            self.assertEquals(len(messages), 0)

            current_date = datetime.date(2015, 4, 12)
            messages = get_filtered_messages(current_date, "javerage")
            self.assertEquals(len(messages), 0)

            current_date = datetime.date(2011, 4, 12)
            messages = get_filtered_messages(current_date, "javerage")
            self.assertEquals(len(messages), 0)
