from unittest2 import TestCase
from myuw.models import BannerMessage
from myuw.dao.messages import get_current_messages
from myuw.test import get_request_with_user, get_request_with_date
import datetime


class TestBannerMessageDAO(TestCase):
    def test_get_current(self):
        BannerMessage.objects.all().delete()

        BannerMessage.objects.create(start=datetime.date(2013, 4, 5),
                                     end=datetime.date(2013, 4, 7),
                                     message_title='test title',
                                     message_body='test body',
                                     affiliation='student')

        request = get_request_with_date('2013-04-04')
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
