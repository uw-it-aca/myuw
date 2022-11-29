# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from myuw.dao.category_notice import get_category_notices
from myuw.dao.notice_mapping import categorize_notices


class TestDegreeNotices(TestCase):

    def test_get_category_notices(self):
        notices = get_category_notices("Degree")
        self.assertEquals(len(notices), 5)
        self.assertEquals(notices[0].notice_category, "Degree")

        notices = get_category_notices("Teaching")
        self.assertEquals(len(notices), 1)

        final_notices = categorize_notices(notices)
        for notice in final_notices:
            self.assertTrue('Graduation' in notice.custom_category)
            self.assertEquals(notice.location_tags[0], 'graduation')
            self.assertFalse(notice.is_critical)
