# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import timedelta
from persistent_message.models import Message, Tag
from django.test import TestCase, override_settings
from myuw.dao.term import get_comparison_datetime_with_tz
from myuw.dao.persistent_messages import BannerMessage
from myuw.test import (get_request_with_user, get_request_with_date)


@override_settings(TIME_ZONE='America/Los_Angeles')
class PersistentMessageDAOTest(TestCase):
    fixtures = ['persistent_messages.json']

    def setup_db(self, req):
        self.message = Message()
        self.message.content = 'Hello World!'
        self.message.begins = (
          get_comparison_datetime_with_tz(req) - timedelta(days=1))
        self.message.save()

    def set_campus(self, msg, campus, affi):
        tag1 = Tag.objects.get(name=campus)
        tag2 = Tag.objects.get(name=affi)
        msg.tags.add(tag1, tag2)
        msg.save()

    def test_tags(self):
        tags = Tag.objects.all()
        self.assertEqual(len(tags), 15)

    def test_get_message(self):
        req = get_request_with_user('javerage')
        self.setup_db(req)
        bm = BannerMessage(req)
        self.assertEqual(len(bm.get_message_json()), 1)

        msgs = Message.objects.all()
        self.assertEqual(len(msgs), 1)
        msg = msgs[0]
        tags = msg.tags.all()
        self.assertTrue(bm._campus_neutral(tags))

        self.set_campus(msg, 'seattle', 'undergraduate')
        tags = msg.tags.all()
        self.assertTrue(bm._is_stud_campus_matched(tags))
        self.assertTrue(bm._student_affiliation_matched(tags))
        self.assertEqual(len(bm.get_message_json()), 1)

    def test_get_message_json(self):
        req = get_request_with_user('jbothell')
        bm = BannerMessage(req)
        self.setup_db(req)
        msgs = Message.objects.all()
        self.set_campus(msgs[0], 'bothell', 'undergraduate')
        tags = msgs[0].tags.all()
        self.assertTrue(bm._is_stud_campus_matched(tags))
        self.assertEqual(len(bm.get_message_json()), 1)
        self.assertEqual(len(bm.get_message_json()), 1)
