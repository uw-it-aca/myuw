# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.conf import settings
from myuw.models import UserNotices
from myuw.dao.notice import get_notices_by_regid


class TestUserNotices(TestCase):
    def test_hash(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        notices = get_notices_by_regid(regid)
        notice = notices[0]
        model = UserNotices()
        hash = model.generate_hash(notice)
        self.assertEqual(hash, "fbb05e8edaf403b7c5eb5a9ac8d7cc3b")
