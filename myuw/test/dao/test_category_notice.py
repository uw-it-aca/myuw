# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from myuw.dao.category_notice import get_category_notices
from myuw.dao.notice_mapping import categorize_notices


class TestDegreeNotices(TestCase):

    def test_get_category_notices(self):
        notices = get_category_notices("Degree")
        self.assertEqual(len(notices), 6)
        self.assertEqual(notices[0].notice_category, "Degree")

        final_notices = categorize_notices(notices)
        for notice in final_notices:
            self.assertTrue('Graduation' in notice.custom_category)
            self.assertEqual(notice.location_tags[0], 'graduation')
            self.assertFalse(notice.is_critical)

        notices = get_category_notices("Teaching")
        self.assertEqual(len(notices), 1)
        cnotices = categorize_notices(notices)
        self.assertEqual(cnotices[0].custom_category,
                          "Teaching ClassResAccessible")
        self.assertEqual(cnotices[0].location_tags[0], 'teaching_summary')
        self.assertFalse(cnotices[0].is_critical)

        notices = get_category_notices("GradeSubmission")
        self.assertEqual(len(notices), 1)
        cnotices = categorize_notices(notices)
        self.assertEqual(cnotices[0].custom_category,
                          "GradeSubmission GradingOpen")
        self.assertEqual(cnotices[0].location_tags[0], 'teaching_summary')
        self.assertFalse(cnotices[0].is_critical)
