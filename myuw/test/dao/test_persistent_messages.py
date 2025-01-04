# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import timedelta
from persistent_message.models import Message, Tag
from django.test import TransactionTestCase, override_settings
from myuw.dao.term import get_comparison_datetime_with_tz
from myuw.dao.persistent_messages import BannerMessage
from myuw.test import (get_request_with_user, get_request_with_date)


def setup_db(req):
    msg = Message()
    msg.content = 'Hello World!'
    msg.begins = (
        get_comparison_datetime_with_tz(req) - timedelta(days=1))
    msg.save()
    return msg


def set_tags(msg, tag_names):
    tags = []
    for tag in tag_names:
        msg.tags.add(Tag.objects.get(name=tag))
    msg.save()
    return msg


class PersistentMessageDAOTest(TransactionTestCase):
    fixtures = ['persistent_messages.json']

    def test_tags(self):
        tags = Tag.objects.all()
        self.assertEqual(len(tags), 15)

    def test_get_message_for_all(self):
        req = get_request_with_user('none')
        bm = BannerMessage(req)
        data = bm.get_message_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["start"], "2013-04-08T07:00:01+00:00")
        self.assertEqual(data[1]["start"], "2013-04-15T07:00:01+00:00")

    def test_get_message_no_match(self):
        req = get_request_with_user('seagrad')
        Message.objects.all().delete()
        msg = setup_db(req)
        msg = set_tags(msg, ['bothell'])
        bm = BannerMessage(req)
        self.assertEqual(len(bm.get_message_json()), 0)

    def test_get_message_for_undergraduate(self):
        req = get_request_with_user('javerage')
        bm = BannerMessage(req)
        msg = setup_db(req)
        msg = set_tags(msg, ['seattle', 'undergraduate'])
        json_content = bm._to_json(msg, True)
        self.assertEqual(json_content['content'], 'Hello World!')
        self.assertEqual(json_content['level_name'], 'Info')
        self.assertEqual(json_content['start'], '2013-04-14T00:00:01-07:00')
        self.assertIsNone(json_content['end'])
        self.assertTrue(json_content['seattle'])
        self.assertTrue(json_content['undergraduate'])

        tags = msg.tags.all()
        self.assertTrue(bm._is_stud_campus_matched(tags))
        self.assertTrue(bm._student_affiliation_matched(tags))
        self.assertEqual(len(bm.get_message_json()), 3)

    def test_get_message_for_faculty(self):
        req = get_request_with_user('bill')
        bm = BannerMessage(req)
        msg = setup_db(req)
        msg = set_tags(msg, ['faculty'])
        tags = msg.tags.all()
        self.assertTrue(bm._employee_affiliation_matched(tags))
        self.assertEqual(len(bm.get_message_json()), 3)

        msg = set_tags(msg, ['seattle'])
        tags = msg.tags.all()
        self.assertTrue(bm._is_employee_campus_matched(tags))
        self.assertEqual(len(bm.get_message_json()), 3)

    def test_get_message_for_alumni(self):
        req = get_request_with_user('jalum')
        bm = BannerMessage(req)
        msg = setup_db(req)
        msg = set_tags(msg, ['alumni'])
        tags = msg.tags.all()
        self.assertTrue(bm._campus_neutral(tags))
        self.assertTrue(bm._for_alumni(tags))
        self.assertEqual(len(bm.get_message_json()), 3)

    def test_get_message_for_applicant(self):
        req = get_request_with_user('japplicant')
        bm = BannerMessage(req)
        msg = setup_db(req)
        msg = set_tags(msg, ['applicant'])
        tags = msg.tags.all()
        self.assertTrue(bm._for_applicant(tags))
        self.assertEqual(len(bm.get_message_json()), 3)
