from django.test import TestCase
from myuw.dao.notice_categorization import NOTICE_CATEGORIES


class TestNoticeCategories(TestCase):

    def test_categories(self):
        categorization = NOTICE_CATEGORIES.get(
            "StudentALR_IntlStuCheckIn", None)
        self.assertIsNotNone(categorization)
        self.assertEqual(categorization["myuw_category"], "Holds")
        self.assertTrue(categorization["critical"])
        self.assertEqual(len(categorization["location_tags"]), 2)

        categorization = NOTICE_CATEGORIES.get(
            "StudentFinAid_AidHoldShort", None)
        self.assertIsNotNone(categorization)
        self.assertEqual(categorization["myuw_category"], "Fees & Finances")
        self.assertFalse(categorization["critical"])
        self.assertEqual(len(categorization["location_tags"]), 1)
