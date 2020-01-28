from django.test import TestCase
import datetime
import csv
from io import StringIO
from myuw.dao.thrive import (
    TARGET_FYP, TARGET_AUT_TRANSFER, TARGET_WIN_TRANSFER,
    _get_offset, _make_urls, _is_displayed, _make_thrive_payload,
    get_current_message, get_previous_messages, get_target_group)
from uw_sws.models import Term
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request_with_user, get_request


@fdao_pws_override
@fdao_sws_override
class TestThrive(TestCase):

    def test_is_target_group(self):
        self.assertIsNone(get_target_group(get_request()))

        request = get_request_with_user('jnew', get_request())
        self.assertEqual(get_target_group(request), "fyp")

        request = get_request_with_user('javg001', get_request())
        self.assertEqual(get_target_group(request), "au_xfer")

        request = get_request_with_user('javg002', get_request())
        self.assertEqual(get_target_group(request), "wi_xfer")

        request = get_request_with_user('javg003', get_request())
        self.assertEqual(get_target_group(request), "au_xfer")
        self.assertFalse(get_target_group(request) == "fyp")

        request = get_request_with_user('javg004', get_request())
        self.assertEqual(get_target_group(request), "wi_xfer")
        self.assertFalse(get_target_group(request) == "au_xfer")

    def test_get_current_message(self):
        request = get_request_with_user('jnew',
                                        get_request_with_date("2017-09-18"))
        message = get_current_message(request)
        self.assertEqual(message['target'], TARGET_FYP)
        self.assertEqual(message['week_label'], 'Week 0')
        self.assertIsNotNone(message['title'])

        request = get_request_with_user('jnew',
                                        get_request_with_date("2017-09-25"))
        message = get_current_message(request)
        self.assertEqual(message['target'], TARGET_FYP)
        self.assertEqual(message['week_label'], 'Week 1')

        request = get_request_with_user('jnew',
                                        get_request_with_date("2017-10-03"))
        message = get_current_message(request)
        self.assertEqual(message['target'], TARGET_FYP)
        self.assertEqual(message['week_label'], 'Week 2')

    def test_get_current_message_aut_transfer(self):
        request = get_request_with_user('javg001',
                                        get_request_with_date("2017-10-03"))
        message = get_current_message(request)
        self.assertEqual(message['target'], TARGET_AUT_TRANSFER)
        self.assertEqual(message['week_label'], 'Week 2')

    def test_get_current_message_win_transfer(self):
        request = get_request_with_user('javg002',
                                        get_request_with_date("2018-01-03"))
        message = get_current_message(request)
        self.assertEqual(message['target'], TARGET_WIN_TRANSFER)
        self.assertEqual(message['week_label'], 'Week 1')

    def test_get_previous_messages(self):
        request = get_request_with_user('jnew',
                                        get_request_with_date("2017-09-24"))
        messages = get_previous_messages(request)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['target'], TARGET_FYP)
        self.assertEqual(messages[0]['week_label'], 'Week 0')

    def test_get_offset(self):
        term = Term()
        term.year = 2013
        term.quarter = "autumn"
        term.first_day_quarter = datetime.date(2013, 9, 11)

        date_prev = datetime.date(2013, 9, 10)
        date_equal = datetime.date(2013, 9, 11)
        date_post = datetime.date(2013, 9, 12)

        offset_prev = _get_offset(date_prev, term)
        self.assertEqual(offset_prev, -1)

        offset_equal = _get_offset(date_equal, term)
        self.assertEqual(offset_equal, 0)

        offset_post = _get_offset(date_post, term)
        self.assertEqual(offset_post, 1)

    def test_make_urls(self):
        one_url_row = '9,11/23/2015,autumn,-10,week_label,category_label,'\
                      'title,this is the message,'\
                      'try this,urlone,http://www.google.com'
        string = StringIO(one_url_row)
        reader = csv.reader(string)
        for row in reader:
            urls = _make_urls(row)
            self.assertEqual(len(urls), 1)

        three_url_row = '9,11/23/2015,autumn,-10,week_label,category_label,'\
                        'title,this is the message,'\
                        'try this,urlone,http://www.google.com,urltwo,' \
                        'http://www.uw.edu,urlthree,http://my.uw.edu'
        string = StringIO(three_url_row)
        reader = csv.reader(string)
        for row in reader:
            urls = _make_urls(row)
            self.assertEqual(len(urls), 3)
            self.assertEqual(urls[0]['title'], "urlone")
            self.assertEqual(urls[0]['href'], "http://www.google.com")
            self.assertEqual(urls[2]['title'], "urlthree")
            self.assertEqual(urls[2]['href'], "http://my.uw.edu")

        no_url_row = '9,11/23/2015,autumn,-10,week_label,category_label,'\
                     'title,this is the message,try this'
        string = StringIO(no_url_row)
        reader = csv.reader(string)
        for row in reader:
            urls = _make_urls(row)
            self.assertEqual(len(urls), 0)

        empty_url_row = '9,11/23/2015,autumn,-10,week_label,category_label,'\
                        'title,this is the message,try this,,,,,,'
        string = StringIO(empty_url_row)
        reader = csv.reader(string)
        for row in reader:
            urls = _make_urls(row)
            self.assertEqual(len(urls), 0)

    def test_is_displayed(self):
        one_url_row = '9,11/23/2015,autumn,-10,week_label,category_label,'\
                      'title,this is the message,try this,urlone,'\
                      'http://www.google.com'
        string = StringIO(one_url_row)
        reader = csv.reader(string)
        for row in reader:
            # Shows after start of display
            self.assertTrue(_is_displayed(row, 'autumn', -9))
            # Shows on start of display
            self.assertTrue(_is_displayed(row, 'autumn', -10))
            # Does not show before start of display
            self.assertFalse(_is_displayed(row, 'autumn', -11))
            # Does not show on incorrect quarter
            self.assertFalse(_is_displayed(row, 'spring', -9))
            # Does not show 7+ days after
            self.assertFalse(_is_displayed(row, 'autumn', -3))

    def test_make_payload(self):
        three_url_row = '9,11/23/2015,autumn,-10,week_label,category_label,'\
                        'title,this is the message,try this,'\
                        'urlone,http://www.google.com,'\
                        'urltwo,http://www.uw.edu,urlthree,http://my.uw.edu'
        string = StringIO(three_url_row)
        reader = csv.reader(string)
        for row in reader:
            payload = _make_thrive_payload(row, TARGET_FYP)
            target_payload = {'message': 'this is the message',
                              'urls': [
                                  {'href': 'http://www.google.com',
                                   'title': 'urlone'},
                                  {'href': 'http://www.uw.edu',
                                   'title': 'urltwo'},
                                  {'href': 'http://my.uw.edu',
                                   'title': 'urlthree'}
                              ],
                              'target': 'fyp',
                              'try_this': 'try this', 'title': 'title',
                              'week_label': 'week_label',
                              'category_label': 'category_label'}
            self.assertDictEqual(payload, target_payload)
